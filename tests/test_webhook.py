import base64
import json
import os
from unittest.mock import patch

from fastapi import status


class TestWebhookRoute:
    """Test cases for the webhook mutating admission controller"""

    def test_create_item_adds_annotation_when_none_exist(self, client):
        """Test adding annotation when no annotations exist"""
        request_data = {
            "uid": "test-uid-123",
            "obj": {"kind": "Pod", "metadata": {"name": "test-pod"}},
            "metadata": {"name": "test-pod", "namespace": "default"},
            "annotations": None,
        }

        response = client.post("/mutate", json=request_data)

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()

        assert response_data["apiVersion"] == "admission.k8s.io/v1"
        assert response_data["kind"] == "AdmissionReview"
        assert response_data["response"]["uid"] == "test-uid-123"
        assert response_data["response"]["allowed"] is True
        assert "patch" in response_data["response"]

        # Decode and verify patch
        patch_data = json.loads(
            base64.b64decode(response_data["response"]["patch"]).decode()
        )
        expected_patch = [
            {
                "op": "add",
                "path": "/metadata/annotations",
                "value": {"example.com/injected": "true"},
            }
        ]
        assert patch_data == expected_patch

    def test_create_item_adds_annotation_when_key_missing(self, client):
        """Test adding annotation when annotations exist but target key is missing"""
        request_data = {
            "uid": "test-uid-456",
            "obj": {"kind": "Pod", "metadata": {"name": "test-pod"}},
            "metadata": {"name": "test-pod", "namespace": "default"},
            "annotations": {"existing.com/annotation": "existing-value"},
        }

        response = client.post("/mutate", json=request_data)

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()

        assert response_data["response"]["allowed"] is True
        assert "patch" in response_data["response"]

        # Decode and verify patch
        patch_data = json.loads(
            base64.b64decode(response_data["response"]["patch"]).decode()
        )
        expected_patch = [
            {
                "op": "add",
                "path": "/metadata/annotations/example.com/injected",
                "value": "true",
            }
        ]
        assert patch_data == expected_patch

    def test_create_item_no_patch_when_annotation_exists(self, client):
        """Test no patch when target annotation already exists with correct value"""
        request_data = {
            "uid": "test-uid-789",
            "obj": {"kind": "Pod", "metadata": {"name": "test-pod"}},
            "metadata": {"name": "test-pod", "namespace": "default"},
            "annotations": {"example.com/injected": "true"},
        }

        response = client.post("/mutate", json=request_data)

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()

        assert response_data["response"]["allowed"] is True
        assert response_data["response"]["patch"] is None

    @patch.dict(os.environ, {"OVERWRITE": "true"})
    def test_create_item_replaces_annotation_when_overwrite_enabled(self, client):
        """Test replacing annotation when OVERWRITE is enabled and value differs"""
        request_data = {
            "uid": "test-uid-replace",
            "obj": {"kind": "Pod", "metadata": {"name": "test-pod"}},
            "metadata": {"name": "test-pod", "namespace": "default"},
            "annotations": {"example.com/injected": "false"},
        }

        response = client.post("/mutate", json=request_data)

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()

        assert response_data["response"]["allowed"] is True
        assert "patch" in response_data["response"]

        # Decode and verify patch
        patch_data = json.loads(
            base64.b64decode(response_data["response"]["patch"]).decode()
        )
        expected_patch = [
            {
                "op": "replace",
                "path": "/metadata/annotations/example.com/injected",
                "value": "true",
            }
        ]
        assert patch_data == expected_patch

    @patch.dict(os.environ, {"OVERWRITE": "false"})
    def test_create_item_no_replace_when_overwrite_disabled(self, client):
        """Test no replacement when OVERWRITE is disabled and value differs"""
        request_data = {
            "uid": "test-uid-no-replace",
            "obj": {"kind": "Pod", "metadata": {"name": "test-pod"}},
            "metadata": {"name": "test-pod", "namespace": "default"},
            "annotations": {"example.com/injected": "false"},
        }

        response = client.post("/mutate", json=request_data)

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()

        assert response_data["response"]["allowed"] is True
        assert response_data["response"]["patch"] is None

    def test_create_item_with_complex_object(self, client):
        """Test with a more complex Kubernetes object"""
        request_data = {
            "uid": "test-uid-complex",
            "obj": {
                "apiVersion": "v1",
                "kind": "Pod",
                "metadata": {
                    "name": "test-pod",
                    "namespace": "default",
                    "labels": {"app": "test"},
                },
                "spec": {
                    "containers": [{"name": "test-container", "image": "nginx:latest"}]
                },
            },
            "metadata": {
                "name": "test-pod",
                "namespace": "default",
                "labels": {"app": "test"},
            },
            "annotations": {"app.kubernetes.io/name": "test-app"},
        }

        response = client.post("/mutate", json=request_data)

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()

        assert response_data["response"]["allowed"] is True
        assert "patch" in response_data["response"]

        # Decode and verify patch adds our annotation
        patch_data = json.loads(
            base64.b64decode(response_data["response"]["patch"]).decode()
        )
        expected_patch = [
            {
                "op": "add",
                "path": "/metadata/annotations/example.com/injected",
                "value": "true",
            }
        ]
        assert patch_data == expected_patch

    def test_create_item_invalid_request_format(self, client):
        """Test handling of invalid request format"""
        invalid_request = {
            "uid": "",  # Invalid: empty UID
            "obj": {},
            "metadata": {},
            "annotations": {},
        }

        response = client.post("/mutate", json=invalid_request)

        # Should return validation error due to empty UID
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_create_item_missing_required_fields(self, client):
        """Test handling of missing required fields"""
        incomplete_request = {
            "uid": "test-uid"
            # Missing obj, metadata, annotations
        }

        response = client.post("/mutate", json=incomplete_request)

        # Should return validation error
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    @patch.dict(os.environ, {"OVERWRITE": "1"})
    def test_overwrite_environment_variable_parsing(self, client):
        """Test that OVERWRITE environment variable is parsed correctly"""
        request_data = {
            "uid": "test-uid-env",
            "obj": {"kind": "Pod", "metadata": {"name": "test-pod"}},
            "metadata": {"name": "test-pod", "namespace": "default"},
            "annotations": {"example.com/injected": "false"},
        }

        response = client.post("/mutate", json=request_data)

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()

        # Should replace because OVERWRITE=1
        assert "patch" in response_data["response"]
        patch_data = json.loads(
            base64.b64decode(response_data["response"]["patch"]).decode()
        )
        assert patch_data[0]["op"] == "replace"
