# STIN Bank (Semester project)
***
## Introduction
Semestrální práce pro předmět STIN

## Features
- [x] 2 Factor Authentication
  - [x] Google authenticator (qrcodes generated on the frontend)
- [x] Multi-currency accounts
- [x] Password change
- [ ] Docker support
- [ ] Tests
- [ ] CI/CD

## Notes for my forgtful ass
- Celery
  - run the worker => celery -A STINBank worker (-l INFO) (-P gevent - pro windejsy)
  - run the scheduler => celery -A STINBank beat (-l INFO)

## Time tracking
### Desktop: 21h
### Laptop: 7.25h