import base64
import json
import os
from logging import getLogger

from fastapi import APIRouter, HTTPException, status

from app.api.di import Container
from app.api.schemas import (
    AdmissionResponse,
    AdmissionReviewRequest,
    AdmissionReviewResponse,
)

# from app.domain.errors import NotFoundError

logger = getLogger(__name__)


def get_router(container: Container) -> APIRouter:
    router = APIRouter(prefix="/mutate", tags=["mutate"])

    @router.post(
        "", response_model=AdmissionReviewResponse, status_code=status.HTTP_201_CREATED
    )
    def create_item(body: AdmissionReviewRequest):
        target_key = "example.com/injected"
        target_value = "true"
        patch_ops = []

        annotations = body.annotations
        uid = body.uid
        obj = body.obj
        metadata = body.metadata

        logger.info("Object: %s", obj)
        logger.info("Metadata: %s", metadata)

        try:
            if annotations is None:
                patch_ops.append(
                    {
                        "op": "add",
                        "path": "/metadata/annotations",
                        "value": {target_key: target_value},
                    }
                )
            else:
                current = annotations.get(target_key)
                if current is None:
                    patch_ops.append(
                        {
                            "op": "add",
                            "path": f"/metadata/annotations/{target_key}",
                            "value": target_value,
                        }
                    )
                else:
                    overwrite = os.getenv("OVERWRITE", "false").lower() in (
                        "1",
                        "true",
                        "yes",
                    )
                    if overwrite and current != target_value:
                        patch_ops.append(
                            {
                                "op": "replace",
                                "path": f"/metadata/annotations/{target_key}",
                                "value": target_value,
                            }
                        )
            if patch_ops:
                patch_b64 = base64.b64encode(json.dumps(patch_ops).encode()).decode()
                response = AdmissionReviewResponse(
                    apiVersion="admission.k8s.io/v1",
                    kind="AdmissionReview",
                    response=AdmissionResponse(
                        uid=uid,
                        allowed=True,
                        patch=patch_b64,
                    ),
                )
            else:
                response = AdmissionReviewResponse(
                    apiVersion="admission.k8s.io/v1",
                    kind="AdmissionReview",
                    response=AdmissionResponse(
                        uid=uid,
                        allowed=True,
                    ),
                )

            logger.info("Added annotation: %s", target_key)
            return response
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return router
