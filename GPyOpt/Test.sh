#nohup python3 TestBCDACK.py  > testACK 2>&1 &
#tail -f testACK
#nohup  python3 ACK_GPyOpt.py  > testACK500 2>&1 &
#tail -f testACK500
nohup  python3 HW_GPyOpt.py  > testHW500 2>&1 &
tail -f testHW500
