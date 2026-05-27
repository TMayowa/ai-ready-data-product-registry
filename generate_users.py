"""Synthetic users, API keys, and approval requests generator."""

import json
import os

from faker import Faker

from src.models import APIKey, ApprovalRequest, User

fake = Faker(["no_NO"])


def _generate_users() -> list[User]:
    names = [fake.name() for _ in range(10)]
    return [
        User(id="USR-001", name=names[0], email=f"{names[0].lower().replace(' ', '.')}@equinor.no",
             role="Platform Admin", department="Data Platform Engineering",
             access_level="Admin", can_approve_data_products=True,
             can_approve_ai_models=True, can_generate_api_keys=True),
        User(id="USR-002", name=names[1], email=f"{names[1].lower().replace(' ', '.')}@equinor.no",
             role="Domain Lead", department="Procurement & Supply Chain",
             domain="Procurement", access_level="Approver",
             can_approve_data_products=True, can_approve_ai_models=True),
        User(id="USR-003", name=names[2], email=f"{names[2].lower().replace(' ', '.')}@equinor.no",
             role="Domain Lead", department="Operations & Maintenance",
             domain="Operations", access_level="Approver",
             can_approve_data_products=True, can_approve_ai_models=True),
        User(id="USR-004", name=names[3], email=f"{names[3].lower().replace(' ', '.')}@equinor.no",
             role="Data Product Owner", department="Procurement Performance & Analytics",
             domain="Procurement", access_level="Contributor",
             can_approve_data_products=True),
        User(id="USR-005", name=names[4], email=f"{names[4].lower().replace(' ', '.')}@equinor.no",
             role="Data Steward", department="Contract Management & Commercial",
             domain="Contract Management", access_level="Contributor"),
        User(id="USR-006", name=names[5], email=f"{names[5].lower().replace(' ', '.')}@equinor.no",
             role="AI Model Owner", department="Supply Chain AI & Analytics",
             access_level="Contributor", can_approve_ai_models=True),
        User(id="USR-007", name=names[6], email=f"{names[6].lower().replace(' ', '.')}@equinor.no",
             role="Governance Lead", department="Data Governance & Compliance",
             access_level="Approver", can_approve_data_products=True,
             can_approve_ai_models=True, can_generate_api_keys=True),
        User(id="USR-008", name=names[7], email=f"{names[7].lower().replace(' ', '.')}@equinor.no",
             role="Data Consumer", department="Category Management",
             domain="Procurement", access_level="Viewer"),
        User(id="USR-009", name=names[8], email=f"{names[8].lower().replace(' ', '.')}@equinor.no",
             role="Data Consumer", department="Offshore Logistics",
             domain="Offshore Logistics", access_level="Viewer"),
        User(id="USR-010", name=names[9], email=f"{names[9].lower().replace(' ', '.')}@equinor.no",
             role="AI Consumer", department="Asset Integrity & Reliability Engineering",
             domain="Operations", access_level="Viewer"),
    ]


def _generate_api_keys() -> list[APIKey]:
    return [
        APIKey(key_id="KEY-001", masked_key="dp_sk_...a8f3", resource_type="data_product",
               resource_id="DP-001", issued_to="USR-008", issued_by="USR-007",
               issued_date="2026-02-01", expires_date="2026-11-01",
               status="Active", rate_limit="1000 requests/hour", scope="read",
               last_used="2026-05-27"),
        APIKey(key_id="KEY-002", masked_key="dp_sk_...c2e9", resource_type="data_product",
               resource_id="DP-002", issued_to="USR-004", issued_by="USR-002",
               issued_date="2025-11-15", expires_date="2026-11-15",
               status="Active", rate_limit="500 requests/hour", scope="read",
               last_used="2026-05-26"),
        APIKey(key_id="KEY-003", masked_key="dp_sk_...f7d1", resource_type="data_product",
               resource_id="DP-003", issued_to="USR-009", issued_by="USR-003",
               issued_date="2026-01-10", expires_date="2026-12-10",
               status="Active", rate_limit="2000 requests/hour", scope="read",
               last_used="2026-05-27"),
        APIKey(key_id="KEY-004", masked_key="dp_sk_...b3a5", resource_type="data_product",
               resource_id="DP-004", issued_to="USR-008", issued_by="USR-007",
               issued_date="2025-05-01", expires_date="2025-11-01",
               status="Expired", rate_limit="2000 requests/hour", scope="read",
               last_used="2025-10-30"),
        APIKey(key_id="KEY-005", masked_key="dp_sk_...e9c2", resource_type="data_product",
               resource_id="DP-005", issued_to="USR-010", issued_by="USR-003",
               issued_date="2026-03-01", expires_date="2026-09-01",
               status="Active", rate_limit="500 requests/hour", scope="read",
               last_used="2026-05-26"),
        APIKey(key_id="KEY-006", masked_key="ai_sk_...d4b8", resource_type="ai_model",
               resource_id="supplier-risk-agent", issued_to="USR-008", issued_by="USR-007",
               issued_date="2026-02-15", expires_date="2026-11-15",
               status="Active", rate_limit="100 requests/hour", scope="read",
               last_used="2026-05-25"),
        APIKey(key_id="KEY-007", masked_key="ai_sk_...7f3a", resource_type="ai_model",
               resource_id="inventory-planning-assistant", issued_to="USR-008", issued_by="USR-007",
               issued_date="2026-01-20", expires_date="2026-10-20",
               status="Active", rate_limit="500 requests/hour", scope="read",
               last_used="2026-05-25"),
        APIKey(key_id="KEY-008", masked_key="ai_sk_...2c6e", resource_type="ai_model",
               resource_id="maintenance-planning-agent", issued_to="USR-010", issued_by="USR-003",
               issued_date="2025-06-01", expires_date="2025-12-01",
               status="Expired", rate_limit="50 requests/hour", scope="read",
               last_used="2025-11-28"),
    ]


def _generate_approval_requests(users: list[User]) -> list[ApprovalRequest]:
    user_map = {u.id: u.name for u in users}
    return [
        ApprovalRequest(
            request_id="REQ-001", request_type="Model promotion",
            resource_id="logistics-disruption-agent",
            resource_name="Logistics Disruption Agent — promotion to Production",
            requested_by="USR-006", requested_date="2026-05-20",
            status="Pending",
            approval_level_required="Governance Lead",
        ),
        ApprovalRequest(
            request_id="REQ-002", request_type="API key generation",
            resource_id="DP-005",
            resource_name="API key for Maintenance Work Order History",
            requested_by="USR-010", requested_date="2026-05-24",
            status="Pending",
            approval_level_required="Domain Lead",
        ),
        ApprovalRequest(
            request_id="REQ-003", request_type="Data product access",
            resource_id="DP-002",
            resource_name="Read access to Contract Spend History",
            requested_by="USR-008", requested_date="2026-04-10",
            status="Approved",
            reviewed_by="USR-002", review_date="2026-04-12",
            review_notes="Approved for read-only access. Category management use case validated.",
            approval_level_required="Domain Lead",
        ),
        ApprovalRequest(
            request_id="REQ-004", request_type="AI model deployment",
            resource_id="inventory-planning-assistant",
            resource_name="Inventory Planning Assistant — production deployment",
            requested_by="USR-006", requested_date="2026-01-05",
            status="Approved",
            reviewed_by="USR-007", review_date="2026-01-18",
            review_notes="Governance review complete. All evaluations passed. Low risk classification confirmed.",
            approval_level_required="Governance Lead",
        ),
        ApprovalRequest(
            request_id="REQ-005", request_type="API key generation",
            resource_id="DP-005",
            resource_name="API key for Maintenance Work Order History (previous request)",
            requested_by="USR-010", requested_date="2026-03-01",
            status="Rejected",
            reviewed_by="USR-003", review_date="2026-03-05",
            review_notes=(
                "Rejected: requester does not have the required data access training certification "
                "for Restricted classification data products. Resubmit after completing EQUINOR-DATA-201 "
                "and EQUINOR-AI-101 training modules."
            ),
            approval_level_required="Domain Lead",
        ),
        ApprovalRequest(
            request_id="REQ-006", request_type="Governance review",
            resource_id="logistics-disruption-agent",
            resource_name="Governance review: Logistics Disruption Agent — safety assessment",
            requested_by="USR-003", requested_date="2026-04-28",
            status="Escalated",
            reviewed_by="USR-002", review_date="2026-05-02",
            review_notes=(
                "Escalated from Domain Lead to Governance Lead. "
                "Safety implications require governance board sign-off due to High risk classification "
                "and potential for safety-critical logistics decisions."
            ),
            approval_level_required="Governance Lead",
        ),
    ]


def main() -> None:
    project_dir = os.path.dirname(os.path.abspath(__file__))

    users = _generate_users()
    api_keys = _generate_api_keys()
    approval_requests = _generate_approval_requests(users)

    for data, filename in [
        (users, "users.json"),
        (api_keys, "api_keys.json"),
        (approval_requests, "approval_requests.json"),
    ]:
        path = os.path.join(project_dir, "data", filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump([item.model_dump(mode="json") for item in data], f, indent=2, ensure_ascii=False)
        print(f"Saved {len(data)} records to {path}")

    print(f"\nUsers: {len(users)} | API Keys: {len(api_keys)} (Active: {sum(1 for k in api_keys if k.status == 'Active')}) | Approvals: {len(approval_requests)}")
    pending = sum(1 for r in approval_requests if r.status == "Pending")
    print(f"Approval statuses: {pending} Pending, {sum(1 for r in approval_requests if r.status == 'Approved')} Approved, {sum(1 for r in approval_requests if r.status == 'Rejected')} Rejected, {sum(1 for r in approval_requests if r.status == 'Escalated')} Escalated")


if __name__ == "__main__":
    main()
