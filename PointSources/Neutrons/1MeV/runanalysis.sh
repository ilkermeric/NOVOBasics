#!/bin/bash

python3 ParseSortPTRAC.py SVSCUnseg.p
python3 ApplyECutOff.py SortedPTRACData 0.01
python3 SegmentHitsSVSC.py SortedPTRACdatawithECutOff 1
python3 CalculateEfficiency.py SegmentedData 0.167 1e7 1.0
python3 DistributionsNoSeg.py SegmentedData 0.167 1e7 1.0
python3 OriginalMultiplicities.py SegmentedData 0.167 1e7 1.0
python3 MultipleInteractions.py SegmentedData 0.167 1e7 1.0
python3 SegmentMultiplicities.py SegmentedData 0.167 1e7 1.0
python3 DistributionsSeg.py SegmentedData 0.167 1e7 1.0 neutron
python3 PlotLoadDistributionSeg.py SegmentedData 0.167 1e7 1.0 1
