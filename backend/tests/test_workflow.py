from datetime import date, timedelta

import pytest


@pytest.mark.asyncio
async def test_full_workflow(client):
    admin_data = {
        "company_name": "TestCo",
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@test.com",
        "role": "employee",
    }
    res = await client.post("/api/v1/auth/register", json=admin_data)
    assert res.status_code == 200
    admin_payload = res.json()["data"]
    admin_temp_pass = admin_payload["temp_password"]
    admin_emp_id = admin_payload["user"]["employee_id"]

    res = await client.post(
        "/api/v1/auth/login",
        json={"email": "admin@test.com", "password": admin_temp_pass},
    )
    assert res.status_code == 200
    admin_tokens = res.json()["data"]
    admin_token = admin_tokens["access_token"]
    admin_refresh = admin_tokens["refresh_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    res = await client.post("/api/v1/auth/refresh", json={"refresh_token": admin_refresh})
    assert res.status_code == 200
    assert res.json()["data"]["access_token"]

    res = await client.post(
        "/api/v1/auth/change-password",
        json={"new_password": "AdminPass123", "confirm_password": "AdminPass123"},
        headers=admin_headers,
    )
    assert res.status_code == 200

    res = await client.get("/api/v1/employees/", headers=admin_headers)
    assert res.status_code == 200
    assert len(res.json()["data"]) == 1

    emp_data = {
        "company_name": "TestCo",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@test.com",
    }
    res = await client.post("/api/v1/auth/register", json=emp_data, headers=admin_headers)
    assert res.status_code == 200
    emp_payload = res.json()["data"]
    emp_temp_pass = emp_payload["temp_password"]
    emp_emp_id = emp_payload["user"]["employee_id"]

    res = await client.post(
        "/api/v1/auth/login",
        json={"email": "john@test.com", "password": emp_temp_pass},
    )
    assert res.status_code == 200
    emp_tokens = res.json()["data"]
    emp_token = emp_tokens["access_token"]
    emp_headers = {"Authorization": f"Bearer {emp_token}"}

    res = await client.post(
        "/api/v1/auth/change-password",
        json={"new_password": "EmpPass123", "confirm_password": "EmpPass123"},
        headers=emp_headers,
    )
    assert res.status_code == 200

    res = await client.put("/api/v1/employees/me", json={"phone": "1234567890"}, headers=emp_headers)
    assert res.status_code == 200
    assert res.json()["data"]["phone"] == "1234567890"

    res = await client.get("/api/v1/employees/me", headers=emp_headers)
    assert res.status_code == 200
    assert res.json()["data"]["employee_id"] == emp_emp_id

    res = await client.post("/api/v1/attendance/check-in", headers=emp_headers)
    assert res.status_code == 200
    assert res.json()["data"]["status"] == "present"

    res = await client.post("/api/v1/attendance/check-out", headers=emp_headers)
    assert res.status_code == 200
    assert res.json()["data"]["check_out"] is not None

    today = date.today()
    res = await client.get(
        f"/api/v1/attendance/me?start_date={today.isoformat()}&end_date={today.isoformat()}",
        headers=emp_headers,
    )
    assert res.status_code == 200
    assert len(res.json()["data"]) == 1

    res = await client.get(
        f"/api/v1/attendance/me/calendar?year={today.year}&month={today.month}",
        headers=emp_headers,
    )
    assert res.status_code == 200
    assert any(day["date"] == today.isoformat() for day in res.json()["data"])

    start = date.today() + timedelta(days=10)
    end = date.today() + timedelta(days=12)
    res = await client.post(
        "/api/v1/leaves/apply",
        json={
            "leave_type": "paid_time_off",
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "reason": "Vacation",
        },
        headers=emp_headers,
    )
    assert res.status_code == 200
    leave_id = res.json()["data"]["id"]

    res = await client.get("/api/v1/leaves/my", headers=emp_headers)
    assert res.status_code == 200
    assert len(res.json()["data"]) == 1

    res = await client.get("/api/v1/leaves/balance", headers=emp_headers)
    assert res.status_code == 200

    res = await client.get("/api/v1/payroll/me", headers=emp_headers)
    assert res.status_code == 200

    res = await client.get("/api/v1/employees/", headers=admin_headers)
    assert res.status_code == 200
    assert len(res.json()["data"]) == 2

    res = await client.get(f"/api/v1/employees/{emp_emp_id}", headers=admin_headers)
    assert res.status_code == 200
    assert res.json()["data"]["employee_id"] == emp_emp_id

    res = await client.get("/api/v1/leaves/", headers=admin_headers)
    assert res.status_code == 200
    assert len(res.json()["data"]) == 1

    res = await client.put(
        f"/api/v1/leaves/{leave_id}",
        json={"status": "approved", "admin_comment": "Approved"},
        headers=admin_headers,
    )
    assert res.status_code == 200
    assert res.json()["data"]["status"] == "approved"

    res = await client.get(f"/api/v1/payroll/{admin_emp_id}", headers=admin_headers)
    assert res.status_code == 200

    res = await client.put(
        f"/api/v1/payroll/{admin_emp_id}",
        json={
            "monthly_wage": 5000.0,
            "basic_salary": 3000.0,
            "hra": 1000.0,
            "allowances": 500.0,
        },
        headers=admin_headers,
    )
    assert res.status_code == 200
    assert res.json()["data"]["monthly_wage"] == 5000.0
    assert res.json()["data"]["gross_salary"] == 4500.0

    res = await client.post(f"/api/v1/payroll/{admin_emp_id}/calculate", headers=admin_headers)
    assert res.status_code == 200

    res = await client.get(f"/api/v1/attendance/summary?date={today.isoformat()}", headers=admin_headers)
    assert res.status_code == 200

    res = await client.post("/api/v1/auth/logout", headers=emp_headers)
    assert res.status_code == 200