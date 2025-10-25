# Security Policy

## Supported Versions

We actively support the following versions of the Kubernetes Mutating Admission Webhook:

| Version | Supported          |
| ------- | ------------------ |
| 1.33.0  | :white_check_mark: |
| 1.32.0  | :white_check_mark: |
| 1.31.0  | :white_check_mark: |
| < 1.31  | :x:                |

## Security Considerations

This project implements a Kubernetes Mutating Admission Webhook that intercepts and modifies Kubernetes resources. Given its privileged position in the cluster, security is paramount.

### Key Security Features

- **TLS Encryption**: All webhook communications are encrypted using TLS
- **Admission Review Validation**: Strict validation of incoming admission review requests
- **Minimal Privileges**: The webhook operates with minimal required permissions
- **Input Sanitization**: All user inputs are validated and sanitized
- **Structured Logging**: Comprehensive logging for security monitoring

### Security Scope

This security policy covers:

- The webhook application code (`app/` directory)
- Container image and Dockerfile
- Kubernetes deployment manifests
- CI/CD pipeline configurations
- Documentation and examples

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability in this project, please report it responsibly.

### How to Report

**Please do NOT create a public GitHub issue for security vulnerabilities.**

Instead, please report security vulnerabilities by:

1. **Email**: Send details to `parraletz@gmail.com`
2. **GitHub Security Advisories**: Use the "Security" tab in this repository
3. **Direct Contact**: Contact the maintainer directly through GitHub

### What to Include

When reporting a vulnerability, please include:

- **Description**: A clear description of the vulnerability
- **Impact**: Potential impact and attack scenarios
- **Reproduction Steps**: Detailed steps to reproduce the issue
- **Proof of Concept**: Code or commands demonstrating the vulnerability (if applicable)
- **Environment**: Kubernetes version, webhook version, and deployment details
- **Suggested Fix**: If you have ideas for fixing the issue

### Response Process

1. **Acknowledgment**: We will acknowledge receipt within 48 hours
2. **Investigation**: We will investigate and assess the vulnerability within 5 business days
3. **Updates**: We will provide regular updates on our progress
4. **Resolution**: We aim to resolve critical vulnerabilities within 30 days
5. **Disclosure**: We will coordinate public disclosure after a fix is available

### Vulnerability Severity

We classify vulnerabilities using the following severity levels:

- **Critical**: Remote code execution, privilege escalation, or cluster compromise
- **High**: Significant security impact affecting multiple users
- **Medium**: Moderate security impact with limited scope
- **Low**: Minor security issues with minimal impact

## Security Best Practices

### For Deployment

- Always use TLS certificates from a trusted CA in production
- Regularly rotate TLS certificates
- Monitor webhook logs for suspicious activity
- Use network policies to restrict webhook access
- Run the webhook with minimal required privileges
- Keep the webhook image updated with latest security patches

### For Development

- Follow secure coding practices
- Validate all inputs thoroughly
- Use dependency scanning tools
- Regularly update dependencies
- Implement comprehensive testing including security tests
- Use static analysis tools to identify potential vulnerabilities

## Security Updates

Security updates will be:

- Released as patch versions (e.g., 1.3.1)
- Documented in the CHANGELOG.md
- Announced through GitHub releases
- Tagged with security labels

## Responsible Disclosure

We follow responsible disclosure practices:

- We will not publicly disclose vulnerabilities until a fix is available
- We will credit security researchers who report vulnerabilities responsibly
- We will provide advance notice to users before public disclosure
- We will coordinate with the Kubernetes security team for cluster-level issues

## Contact

For security-related questions or concerns:

- Security Email: `parraletz@gmail.com`
- Maintainer: [@parraletz](https://github.com/parraletz)
- Project Issues: Use GitHub Security Advisories for vulnerabilities

---

_This security policy is effective as of October 2025 and may be updated periodically._
