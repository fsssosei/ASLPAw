# ASLPAw

![PyPI](https://img.shields.io/pypi/v/ASLPAw?color=red)
![PyPI - Status](https://img.shields.io/pypi/status/ASLPAw)
![GitHub Release Date](https://img.shields.io/github/release-date/fsssosei/ASLPAw)
[![Build Status](https://scrutinizer-ci.com/g/fsssosei/ASLPAw/badges/build.png?b=master)](https://scrutinizer-ci.com/g/fsssosei/ASLPAw/build-status/master)
[![Code Intelligence Status](https://scrutinizer-ci.com/g/fsssosei/ASLPAw/badges/code-intelligence.svg?b=master)](https://scrutinizer-ci.com/code-intelligence)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/fsssosei/ASLPAw.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/fsssosei/ASLPAw/context:python)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/e85d538645c44b9e87bf16448a9ac6f1)](https://www.codacy.com/manual/fsssosei/ASLPAw?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=fsssosei/ASLPAw&amp;utm_campaign=Badge_Grade)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/fsssosei/ASLPAw/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/fsssosei/ASLPAw/?branch=master)
![PyPI - Downloads](https://img.shields.io/pypi/dw/ASLPAw?label=PyPI%20-%20Downloads)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ASLPAw)
![PyPI - License](https://img.shields.io/pypi/l/ASLPAw)

*Adaptive overlapping community discovery algorithm package in python.*

*Welcome to complete the documentation.*

## Installation

Installation can be done through pip. You must have python version >= 3.6.

	pip install ASLPAw

## Usage

The statement to import the package:

	from ASLPAw_package import ASLPAw
	
Example:

	>>> from networkx.generators.community import relaxed_caveman_graph
	>>> data_graph = relaxed_caveman_graph(3, 6, 0.22, seed = 65535)
	>>> ASLPAw(data_graph, seed=65535).adj
	AdjacencyView({0: {1: {'weight': 30}}, 1: {6: {'weight': 15}, 1: {'weight': 14}}, 6: {6: {'weight': 31}}, 2: {1: {'weight': 30}}, 3: {1: {'weight': 29}}, 4: {1: {'weight': 30}}, 5: {1: {'weight': 30}}, 7: {6: {'weight': 30}}, 8: {6: {'weight': 29}}, 9: {6: {'weight': 29}}, 10: {6: {'weight': 25}}, 11: {6: {'weight': 28}}, 12: {15: {'weight': 19}}, 15: {15: {'weight': 24}}, 13: {15: {'weight': 22}}, 14: {15: {'weight': 22}}, 16: {15: {'weight': 19}}, 17: {15: {'weight': 19}}})
	
	>>> data_graph = relaxed_caveman_graph(3, 6, 0.39, seed = 65535)
	>>> ASLPAw(data_graph, seed=65535).adj
	AdjacencyView({0: {3: {'weight': 25}}, 3: {3: {'weight': 27}}, 1: {3: {'weight': 26}}, 2: {3: {'weight': 28}}, 4: {3: {'weight': 29}}, 5: {3: {'weight': 29}}, 6: {6: {'weight': 30}}, 7: {6: {'weight': 30}}, 8: {6: {'weight': 21}}, 9: {6: {'weight': 27}}, 10: {3: {'weight': 20}}, 11: {6: {'weight': 27}}, 12: {15: {'weight': 16}, 6: {'weight': 13}}, 15: {}, 13: {6: {'weight': 19}}, 14: {6: {'weight': 20}}, 16: {15: {'weight': 17}, 6: {'weight': 12}}, 17: {15: {'weight': 18}, 6: {'weight': 12}}})
