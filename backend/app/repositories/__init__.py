"""Repository write functions are deliberately not exported at package
level. `add()` in `audit_record_repository.py` is an internal mechanism
of `AuditService.record(...)`, not an application-code entry point --
see that module's docstring.
"""
