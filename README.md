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

ASLPAw can be used for disjoint and overlapping community detection and works on weighted/unweighted and directed/undirected networks.
ASLPAw is adaptive with virtually no configuration parameters.

This is an easy-to-understand reference implementation that is not optimized for efficiency, but is robust. The underlying NetworkX package is inherently inefficient and unsuitable for use on large networks.
The next release will extend support for multiple productivity packages, such as SNAP, graph-tool, and igraph.

## Installation

Installation can be done through pip. You must have python version >= 3.8

	pip install ASLPAw

## Usage

The statement to import the package:

	from ASLPAw_package import ASLPAw
	
Example:

	>>> from networkx.generators.community import relaxed_caveman_graph
	
	>>> #Set seed to make the results repeatable.
	>>> data_graph = relaxed_caveman_graph(3, 6, 0.22, seed = 65535)
	>>> ASLPAw(data_graph, seed=65535).adj
	AdjacencyView({0: {2: {'weight': 0.9}}, 2: {2: {'weight': 0.9333333333333333}}, 1: {6: {'weight': 0.6}}, 6: {6: {'weight': 1.0}}, 3: {2: {'weight': 0.6}}, 4: {2: {'weight': 0.8666666666666667}}, 5: {2: {'weight': 0.9333333333333333}}, 7: {6: {'weight': 1.0}}, 8: {6: {'weight': 0.9666666666666667}}, 9: {6: {'weight': 0.9333333333333333}}, 10: {6: {'weight': 0.8666666666666667}}, 11: {6: {'weight': 0.9666666666666667}}, 12: {12: {'weight': 1.0333333333333334}}, 13: {12: {'weight': 0.9666666666666667}}, 14: {12: {'weight': 1.0}}, 15: {12: {'weight': 1.0}}, 16: {12: {'weight': 1.0}}, 17: {12: {'weight': 1.0}}})
	
	>>> data_graph = relaxed_caveman_graph(3, 6, 0.39, seed = 65535)
	>>> ASLPAw(data_graph, seed=65535).adj
	AdjacencyView({0: {1: {'weight': 0.9333333333333333}}, 1: {1: {'weight': 1.0}}, 2: {1: {'weight': 1.0}}, 3: {1: {'weight': 0.9666666666666667}}, 4: {1: {'weight': 1.0}}, 5: {1: {'weight': 0.9666666666666667}}, 6: {}, 7: {7: {'weight': 0.7666666666666667}}, 8: {}, 9: {13: {'weight': 0.4}, 6: {'weight': 0.26666666666666666}}, 13: {13: {'weight': 0.6333333333333333}}, 10: {1: {'weight': 0.5666666666666667}}, 11: {7: {'weight': 0.6333333333333333}}, 12: {12: {'weight': 0.4666666666666667}, 13: {'weight': 0.4}}, 14: {13: {'weight': 0.5666666666666667}}, 15: {13: {'weight': 0.5333333333333333}, 12: {'weight': 0.3333333333333333}}, 16: {13: {'weight': 0.43333333333333335}}, 17: {13: {'weight': 0.43333333333333335}, 12: {'weight': 0.4}}})
