#!/usr/bin/env python3

import matplotlib.pyplot as plt
import pandas as pd

# Inline log data
log_text = """
  fs-file-reader    6439 [001]  3399.871468:                     syscalls:sys_enter_openat: dfd: 0xffffff9c, filename: 0x7ffe43867573, flags: 0x00000000, mode: 0x00000000
  fs-file-reader    6439 [001]  3399.871508:              ext4:ext4_es_lookup_extent_enter: dev 254,1 ino 13369352 lblk 0
  fs-file-reader    6439 [001]  3399.871509:               ext4:ext4_es_lookup_extent_exit: dev 254,1 ino 13369352 found 1 [0/1) 53485607 WR
  fs-file-reader    6439 [001]  3399.871518:              ext4:ext4_es_lookup_extent_enter: dev 254,1 ino 13369352 lblk 2
  fs-file-reader    6439 [001]  3399.871519:               ext4:ext4_es_lookup_extent_exit: dev 254,1 ino 13369352 found 1 [1/2) 53486259 WR
  fs-file-reader    6439 [001]  3399.871548:              ext4:ext4_es_lookup_extent_enter: dev 254,1 ino 13369353 lblk 0
  fs-file-reader    6439 [001]  3399.871549:               ext4:ext4_es_lookup_extent_exit: dev 254,1 ino 13369353 found 0 [0/0) 0 
  fs-file-reader    6439 [001]  3399.871551:                ext4:ext4_ext_map_blocks_enter: dev 254,1 ino 13369353 lblk 0 len 1 flags 
  fs-file-reader    6439 [001]  3399.871563:          filemap:mm_filemap_add_to_page_cache: dev 0:3 ino fe00001 pfn=0x127ef6 ofs=219079520256 order=0
  fs-file-reader    6439 [001]  3399.871568:                     ext4:ext4_ext_load_extent: dev 254,1 ino 13369353 lblk 53486211 pblk 18446744072648992008
  fs-file-reader    6439 [001]  3399.871573:                         block:block_bio_queue: 254,1 R 427889688 + 8 [fs-file-reader]
  fs-file-reader    6439 [001]  3399.871581:                         block:block_bio_remap: 254,0 R 427891736 + 8 <- (254,1) 427889688
  fs-file-reader    6439 [001]  3399.871582:                         block:block_bio_queue: 254,0 R 427891736 + 8 [fs-file-reader]
  fs-file-reader    6439 [001]  3399.871589:                         block:block_bio_remap: 259,0 R 427924504 + 8 <- (254,0) 427891736
  fs-file-reader    6439 [001]  3399.871589:                         block:block_bio_remap: 259,0 R 429974552 + 8 <- (259,3) 427924504
  fs-file-reader    6439 [001]  3399.871590:                         block:block_bio_queue: 259,0 R 429974552 + 8 [fs-file-reader]
  fs-file-reader    6439 [001]  3399.871597:                             block:block_getrq: 259,0 R 429974552 + 8 [fs-file-reader]
  fs-file-reader    6439 [001]  3399.871598:                          block:block_io_start: 259,0 R 4096 () 429974552 + 8 [fs-file-reader]
  fs-file-reader    6439 [001]  3399.871600:                              block:block_plug: [fs-file-reader]
  fs-file-reader    6439 [001]  3399.871612:                          block:block_rq_issue: 259,0 R 4096 () 429974552 + 8 [fs-file-reader]
  fs-file-reader    6439 [001]  3399.871623:                            sched:sched_switch: fs-file-reader:6439 [120] D ==> swapper/1:0 [120]
  fs-file-reader    6439 [001]  3399.872347:                     ext4:ext4_es_cache_extent: dev 254,1 ino 13369353 es [0/1) mapped 53485608 status W
  fs-file-reader    6439 [001]  3399.872349:                     ext4:ext4_es_cache_extent: dev 254,1 ino 13369353 es [1/2) mapped 53486153 status W
  fs-file-reader    6439 [001]  3399.872350:                     ext4:ext4_es_cache_extent: dev 254,1 ino 13369353 es [3/2) mapped 53486188 status W
  fs-file-reader    6439 [001]  3399.872351:                     ext4:ext4_es_cache_extent: dev 254,1 ino 13369353 es [5/1) mapped 53486208 status W
  fs-file-reader    6439 [001]  3399.872352:                     ext4:ext4_es_cache_extent: dev 254,1 ino 13369353 es [6/1) mapped 53486210 status W
  fs-file-reader    6439 [001]  3399.872353:                     ext4:ext4_es_cache_extent: dev 254,1 ino 13369353 es [7/1) mapped 53486214 status W
  fs-file-reader    6439 [001]  3399.872354:                     ext4:ext4_es_cache_extent: dev 254,1 ino 13369353 es [8/1) mapped 53486220 status W
  fs-file-reader    6439 [001]  3399.872355:                     ext4:ext4_es_cache_extent: dev 254,1 ino 13369353 es [9/1) mapped 53486235 status W
  fs-file-reader    6439 [001]  3399.872356:                     ext4:ext4_es_cache_extent: dev 254,1 ino 13369353 es [10/1) mapped 53486244 status W
  fs-file-reader    6439 [001]  3399.872356:                     ext4:ext4_es_cache_extent: dev 254,1 ino 13369353 es [11/1) mapped 53486282 status W
  fs-file-reader    6439 [001]  3399.872357:                     ext4:ext4_es_cache_extent: dev 254,1 ino 13369353 es [12/3) mapped 53486318 status W
  fs-file-reader    6439 [001]  3399.872358:                     ext4:ext4_es_cache_extent: dev 254,1 ino 13369353 es [15/1) mapped 53486346 status W
  fs-file-reader    6439 [001]  3399.872359:                     ext4:ext4_es_cache_extent: dev 254,1 ino 13369353 es [16/1) mapped 53486363 status W
  fs-file-reader    6439 [001]  3399.872359:                     ext4:ext4_es_cache_extent: dev 254,1 ino 13369353 es [17/1) mapped 53486703 status W
  fs-file-reader    6439 [001]  3399.872360:                     ext4:ext4_es_cache_extent: dev 254,1 ino 13369353 es [18/1) mapped 75071659 status W
  fs-file-reader    6439 [001]  3399.872361:                     ext4:ext4_es_cache_extent: dev 254,1 ino 13369353 es [19/1) mapped 87359569 status W
  fs-file-reader    6439 [001]  3399.872362:                     ext4:ext4_es_cache_extent: dev 254,1 ino 13369353 es [20/1) mapped 87228447 status W
  fs-file-reader    6439 [001]  3399.872363:                     ext4:ext4_es_cache_extent: dev 254,1 ino 13369353 es [21/1) mapped 87228446 status W
  fs-file-reader    6439 [001]  3399.872364:                     ext4:ext4_es_cache_extent: dev 254,1 ino 13369353 es [22/2) mapped 87228458 status W
  fs-file-reader    6439 [001]  3399.872364:                     ext4:ext4_es_cache_extent: dev 254,1 ino 13369353 es [24/2) mapped 87228444 status W
  fs-file-reader    6439 [001]  3399.872366:                     ext4:ext4_ext_show_extent: dev 254,1 ino 13369353 lblk 0 pblk 53485608 len 1
  fs-file-reader    6439 [001]  3399.872367:                 ext4:ext4_ext_map_blocks_exit: dev 254,1 ino 13369353 flags  lblk 0 pblk 53485608 len 1 mflags M ret 1
  fs-file-reader    6439 [001]  3399.872369:                    ext4:ext4_es_insert_extent: dev 254,1 ino 13369353 es [0/1) mapped 53485608 status W
  fs-file-reader    6439 [001]  3399.872375:          filemap:mm_filemap_add_to_page_cache: dev 0:3 ino fe00001 pfn=0x14a007 ofs=219077050368 order=0
  fs-file-reader    6439 [001]  3399.872378:                         block:block_bio_queue: 254,1 RM 427884864 + 8 [fs-file-reader]
  fs-file-reader    6439 [001]  3399.872379:                         block:block_bio_remap: 254,0 RM 427886912 + 8 <- (254,1) 427884864
  fs-file-reader    6439 [001]  3399.872380:                         block:block_bio_queue: 254,0 RM 427886912 + 8 [fs-file-reader]
  fs-file-reader    6439 [001]  3399.872382:                         block:block_bio_remap: 259,0 RM 427919680 + 8 <- (254,0) 427886912
  fs-file-reader    6439 [001]  3399.872383:                         block:block_bio_remap: 259,0 RM 429969728 + 8 <- (259,3) 427919680
  fs-file-reader    6439 [001]  3399.872383:                         block:block_bio_queue: 259,0 RM 429969728 + 8 [fs-file-reader]
  fs-file-reader    6439 [001]  3399.872385:                             block:block_getrq: 259,0 RM 429969728 + 8 [fs-file-reader]
  fs-file-reader    6439 [001]  3399.872386:                          block:block_io_start: 259,0 RM 4096 () 429969728 + 8 [fs-file-reader]
  fs-file-reader    6439 [001]  3399.872387:                              block:block_plug: [fs-file-reader]
  fs-file-reader    6439 [001]  3399.872389:                          block:block_rq_issue: 259,0 RM 4096 () 429969728 + 8 [fs-file-reader]
  fs-file-reader    6439 [001]  3399.872392:                            sched:sched_switch: fs-file-reader:6439 [120] D ==> swapper/1:0 [120]
  fs-file-reader    6439 [001]  3399.872732:              ext4:ext4_es_lookup_extent_enter: dev 254,1 ino 13369353 lblk 21
  fs-file-reader    6439 [001]  3399.872733:               ext4:ext4_es_lookup_extent_exit: dev 254,1 ino 13369353 found 1 [21/1) 87228446 W
  fs-file-reader    6439 [001]  3399.872740:          filemap:mm_filemap_add_to_page_cache: dev 0:3 ino fe00001 pfn=0x13c8f2 ofs=357287714816 order=0
  fs-file-reader    6439 [001]  3399.872742:                         block:block_bio_queue: 254,1 RM 697827568 + 8 [fs-file-reader]
  fs-file-reader    6439 [001]  3399.872743:                         block:block_bio_remap: 254,0 RM 697829616 + 8 <- (254,1) 697827568
  fs-file-reader    6439 [001]  3399.872744:                         block:block_bio_queue: 254,0 RM 697829616 + 8 [fs-file-reader]
  fs-file-reader    6439 [001]  3399.872745:                         block:block_bio_remap: 259,0 RM 697862384 + 8 <- (254,0) 697829616
  fs-file-reader    6439 [001]  3399.872746:                         block:block_bio_remap: 259,0 RM 699912432 + 8 <- (259,3) 697862384
  fs-file-reader    6439 [001]  3399.872747:                         block:block_bio_queue: 259,0 RM 699912432 + 8 [fs-file-reader]
  fs-file-reader    6439 [001]  3399.872748:                             block:block_getrq: 259,0 RM 699912432 + 8 [fs-file-reader]
  fs-file-reader    6439 [001]  3399.872749:                          block:block_io_start: 259,0 RM 4096 () 699912432 + 8 [fs-file-reader]
  fs-file-reader    6439 [001]  3399.872749:                              block:block_plug: [fs-file-reader]
  fs-file-reader    6439 [001]  3399.872751:                          block:block_rq_issue: 259,0 RM 4096 () 699912432 + 8 [fs-file-reader]
  fs-file-reader    6439 [001]  3399.872754:                            sched:sched_switch: fs-file-reader:6439 [120] D ==> swapper/1:0 [120]
  fs-file-reader    6439 [001]  3399.923075:              ext4:ext4_es_lookup_extent_enter: dev 254,1 ino 13371895 lblk 0
  fs-file-reader    6439 [001]  3399.923080:               ext4:ext4_es_lookup_extent_exit: dev 254,1 ino 13371895 found 0 [0/0) 0 
  fs-file-reader    6439 [001]  3399.923081:                ext4:ext4_ext_map_blocks_enter: dev 254,1 ino 13371895 lblk 0 len 1 flags 
  fs-file-reader    6439 [001]  3399.923083:                     ext4:ext4_es_cache_extent: dev 254,1 ino 13371895 es [0/1) mapped 53485978 status W
  fs-file-reader    6439 [001]  3399.923086:                     ext4:ext4_ext_show_extent: dev 254,1 ino 13371895 lblk 0 pblk 53485978 len 1
  fs-file-reader    6439 [001]  3399.923087:                 ext4:ext4_ext_map_blocks_exit: dev 254,1 ino 13371895 flags  lblk 0 pblk 53485978 len 1 mflags M ret 1
  fs-file-reader    6439 [001]  3399.923088:                    ext4:ext4_es_insert_extent: dev 254,1 ino 13371895 es [0/1) mapped 53485978 status W
  fs-file-reader    6439 [001]  3399.923102:          filemap:mm_filemap_add_to_page_cache: dev 0:3 ino fe00001 pfn=0x148c91 ofs=219078565888 order=0
  fs-file-reader    6439 [001]  3399.923110:                         block:block_bio_queue: 254,1 RM 427887824 + 8 [fs-file-reader]
  fs-file-reader    6439 [001]  3399.923116:                         block:block_bio_remap: 254,0 RM 427889872 + 8 <- (254,1) 427887824
  fs-file-reader    6439 [001]  3399.923117:                         block:block_bio_queue: 254,0 RM 427889872 + 8 [fs-file-reader]
  fs-file-reader    6439 [001]  3399.923121:                         block:block_bio_remap: 259,0 RM 427922640 + 8 <- (254,0) 427889872
  fs-file-reader    6439 [001]  3399.923121:                         block:block_bio_remap: 259,0 RM 429972688 + 8 <- (259,3) 427922640
  fs-file-reader    6439 [001]  3399.923122:                         block:block_bio_queue: 259,0 RM 429972688 + 8 [fs-file-reader]
  fs-file-reader    6439 [001]  3399.923128:                             block:block_getrq: 259,0 RM 429972688 + 8 [fs-file-reader]
  fs-file-reader    6439 [001]  3399.923129:                          block:block_io_start: 259,0 RM 4096 () 429972688 + 8 [fs-file-reader]
  fs-file-reader    6439 [001]  3399.923130:                              block:block_plug: [fs-file-reader]
  fs-file-reader    6439 [001]  3399.923139:                          block:block_rq_issue: 259,0 RM 4096 () 429972688 + 8 [fs-file-reader]
  fs-file-reader    6439 [001]  3399.923147:                            sched:sched_switch: fs-file-reader:6439 [120] D ==> swapper/1:0 [120]
  fs-file-reader    6439 [001]  3399.923555:                      syscalls:sys_exit_openat: 0x3
"""

# Parse log text to extract times and full event descriptions
times = []
full_events = []

for line in log_text.strip().split('\n'):
    parts = line.split()
    time = float(parts[3].strip(':'))
    full_event = ' '.join(parts[4:])  # Extract the full event description
    print(full_event)
    times.append(time)
    full_events.append(full_event)

# Calculate time differences based on the previous event, starting with a 0 for the first entry
time_diffs = [0] + [times[i] - times[i - 1] for i in range(1, len(times))]

# Create DataFrame for plotting
df = pd.DataFrame({
    'Event': full_events,
    'Time Difference': time_diffs
})

# Plot with the object-oriented interface and customizations
fig, ax = plt.subplots(figsize=(20, 14))  # Larger figure to allow for long labels
ax.barh(df['Event'], df['Time Difference'])
#ax.set_xlabel('Time Difference (seconds)')
#ax.set_ylabel('Event')
#ax.set_title('Time Differences Between Events')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.xaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
ax.invert_yaxis()  # Rotate the chart to 90 degrees
plt.subplots_adjust(left=0.65)  # Increase left margin for longer labels
plt.savefig("output.pdf")
plt.close()

