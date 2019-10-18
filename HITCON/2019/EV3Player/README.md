# EV3 Player

## Payload

```sh
tshark -r ev3_player.pklg -Y 'btrfcomm && data.data' -T fields -e data.data  > dump
python analysis.py
```

The flag is in recovered `ag.rso`.

`hitcon{playsoundwithlegomindstormsrobot}`