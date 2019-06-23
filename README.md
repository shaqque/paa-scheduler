# PAA Scheduler

Tool to help schedule appointments between new Rice students and Divisional Advisers during O-Week as part of the PAA Program

## Background

Every year, new students at Rice University go through [O-Week](https://success.rice.edu/first-year-programs/o-week) to help them better understand and prepare for university life. As part of this, the PAA program selects 4 [O-Week PAAs](https://oaa.rice.edu/paa-application), or Peer Academic Advisers, per college who help new students navigate the specifics of the academics at Rice.

Part of the responsiblities of a PAA is scheduling appointments between students and divisional advisers who are effectively the point person of a division of study for each college. This was done manually, which becomes a bigger problem considering there are ~100 students to plan for, and they'd have to be grouped by major within each division. To make things more difficult, new students are often indecisive and may change their major closer to the date of actual appointments, and they would want to meet with the right divisional adviser for that major.

This tool aims to automate all that and allow PAAs to focus on improving other aspects of the O-Week Advising.

## How to use

In its current version, the paa-scheduler needs 3 [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) files, which are as follows:

* Student-major information       --- name of student, intended major
* Major-department information    --- major, department the major belongs to
* Department-adviser information  --- department, name of divisional adviser

The directories of these files will have to be specified in `scheduler.py`, and running scheduler will then output a csv file containing the following for each student, in order:

```divisional adviser, time slot, name of student, major```

## Status of project

The tool works as it is currently, but may be modified to fit actual use during 2019 O-Week (at McMurtry College). 

The eventual goal is to standardize and distribute this tool for future PAA use, so that PAAs can focus on other parts of the program that can directly enhance the new students' O-Week experience. 
