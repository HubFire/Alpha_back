# -*- coding: utf-8 -*-
"""
Created on Tue Apr 05 09:02:46 2016

@author: HUYI
"""
import pandas as pd


def prepare_data(args):
    read_path='/root/Desktop/tmp/'+args[0]+'.csv'
    write_path='/root/Desktop/tmp/'+'temp.csv'
    df = pd.read_csv(read_path, index_col=0)
    df.sort_index(axis=0,  ascending=True)

    start = pd.Period(args[1])
    end = pd.Period(args[2])

    df = df[df.index>=str(start)]
    df = df[df.index<=str(end)]
    df.to_csv(write_path)
    return df

args = ["orcl", "2008-01-02", "2008-03-03", "1000000", "day"]
prepare_data(args)
