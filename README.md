\# SecureCI



\## Automated DevSecOps Security Scanner



SecureCI is a local security scanning tool that helps developers find common security problems in their projects before deployment.



It can scan a public GitHub repository and generate a security report through a local web dashboard.



\---



\## Features



SecureCI currently supports:



\- Secret detection using Gitleaks

\- Source-code security scanning using Semgrep

\- Python dependency vulnerability scanning using pip-audit

\- Security Gate

\- Detailed vulnerability report

\- Local web dashboard

\- GitHub repository scanning

\- Rescan support



\---



\## How SecureCI Works



```text

GitHub Repository

\&#x20;      |

\&#x20;      v

\&#x20;  SecureCI

\&#x20;      |

\&#x20;      +---- Gitleaks

\&#x20;      |

\&#x20;      +---- Semgrep

\&#x20;      |

\&#x20;      +---- pip-audit

\&#x20;      |

\&#x20;      v

\&#x20;Security Report

\&#x20;      |

\&#x20;      v

\&#x20;Security Gate

\&#x20;      |

\&#x20;      +---- PASS

\&#x20;      |

\&#x20;      +---- BLOCKED

\&#x20;      |

\&#x20;      v

\&#x20;Local Dashboard


