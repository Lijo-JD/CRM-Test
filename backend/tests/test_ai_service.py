from app.services.ai_service import ask_crm_secure, validate_sql


def test_validate_sql_rejects_dangerous_queries():
    try:
        validate_sql('DROP TABLE customers')
        assert False, 'Expected DROP to be blocked'
    except ValueError:
        pass


def test_ask_crm_secure_rejects_out_of_scope_requests(monkeypatch):
    def fake_intent(_):
        return 'NO'

    monkeypatch.setattr('app.services.ai_service.classify_intent', fake_intent)
    result = ask_crm_secure('How to cook pasta?')
    assert result['allowed'] is False
    assert 'CRM assistant' in result['message']


def test_ask_crm_secure_generates_sql_for_valid_queries(monkeypatch):
    monkeypatch.setattr('app.services.ai_service.classify_intent', lambda _q: 'YES')
    monkeypatch.setattr('app.services.ai_service.generate_sql', lambda _q: 'SELECT * FROM customers LIMIT 1')
    monkeypatch.setattr('app.services.ai_service.execute_sql_with_retry', lambda _sql, _question: {'message': 'Operation successful'})
    result = ask_crm_secure('Show one customer')
    assert result['allowed'] is True
    assert result['generated_sql'] == 'SELECT * FROM customers LIMIT 1'
