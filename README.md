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
- [x] Tests
- [ ] CI/CD

## Notes for my forgtful ass
- Celery
  - run the worker => celery -A STINBank worker (-l INFO) (-P gevent - pro windejsy)
  - run the scheduler => celery -A STINBank beat (-l INFO)

## Time tracking
### Desktop: 35h
### Laptop: 10.25h

[![codecov](https://codecov.io/gh/Pzdrs/STIN-bank/branch/develop/graph/badge.svg?token=CW5L04S0IJ)](https://codecov.io/gh/Pzdrs/STIN-bank)