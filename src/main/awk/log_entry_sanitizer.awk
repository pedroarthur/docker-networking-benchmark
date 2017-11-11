#!/usr/bin/awk -f
{
  FS=",";
  split($7, range, "-");

  s=sprintf("%03d", range[1]);
  e=sprintf("%03d", range[2]);

  print $2, $3, $4, $5, $6, s, e, $8 / 1048576
}
