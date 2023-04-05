# STIN Bank (Semester project)
***
## Introduction
Semestrální práce pro předmět STIN

## Features
- [ ] 2 Factor Authentication
- [ ] Multi-currency accounts

## Notes for my forgtful ass
- Celery
  - run the worker => celery -A STINBank worker (-l INFO) (-P gevent - pro windejsy)
  - run the scheduler => celery -A STINBank beat (-l INFO)