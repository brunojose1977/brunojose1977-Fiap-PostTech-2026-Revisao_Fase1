#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ponto de entrada exigido pelo Buildozer / python-for-android.

No Android o aplicativo sempre inicia por um arquivo chamado ``main.py``.
Aqui apenas importamos e executamos o jogo definido em
``fiap_postech_quiz.py``, mantendo um único código-fonte para desktop e mobile.
"""

from fiap_postech_quiz import main

if __name__ == "__main__":
    main()
