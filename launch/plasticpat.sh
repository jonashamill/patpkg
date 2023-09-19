#!/bin/bash

roslaunch patpkg plasticpat.launch 2> >(grep -v TF_REPEATED_DATA buffer_core)
