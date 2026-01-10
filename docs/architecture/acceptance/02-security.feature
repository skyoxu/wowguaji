Feature: 02 Security Baseline (Godot 4.5, Windows-only)

  References:
    - ADR-0019 (Godot security baseline)
    - docs/architecture/base/02-security-baseline-godot-v2.md
    - docs/architecture/base/03-observability-sentry-logging-v2.md (audit artifacts under logs/**)

  Scenario: Default deny in secure mode
    Given GD_SECURE_MODE is "1"
    When a security-sensitive capability is requested
    Then the request is denied by default
    And an audit entry is written under "logs/**"

  Scenario: External URL allowlist - allow https host
    Given GD_SECURE_MODE is "1"
    And GD_OFFLINE_MODE is "0"
    And ALLOWED_EXTERNAL_HOSTS is "example.com,sentry.io"
    When the game requests opening external URL "https://example.com/path"
    Then the request is allowed
    And an audit entry is written under "logs/**"

  Scenario: External URL allowlist - deny non-https scheme
    Given GD_SECURE_MODE is "1"
    And ALLOWED_EXTERNAL_HOSTS is "example.com"
    When the game requests opening external URL "http://example.com/path"
    Then the request is denied
    And an audit entry is written under "logs/**"

  Scenario: External URL allowlist - deny non-whitelisted host
    Given GD_SECURE_MODE is "1"
    And ALLOWED_EXTERNAL_HOSTS is "example.com"
    When the game requests opening external URL "https://evil.example.net/"
    Then the request is denied
    And an audit entry is written under "logs/**"

  Scenario: Offline mode denies all outbound access
    Given GD_SECURE_MODE is "1"
    And GD_OFFLINE_MODE is "1"
    And ALLOWED_EXTERNAL_HOSTS is "example.com"
    When the game requests opening external URL "https://example.com/"
    Then the request is denied
    And an audit entry is written under "logs/**"
