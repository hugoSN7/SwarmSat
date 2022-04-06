Description of the public data collected with iMotes in the roller tour in Paris. See RollerNet: http://rollernet.lip6.fr/

========================
I Terms and conditions: 
========================

- You are welcome to use these traces for your research. We ask you in
return to accept the following terms:
 
 1- To acknowledge the use of the data in all resulting publications. 

Please reference the following paper:
 
@InProceedings{RollerNet-INFOCOM09,
	author = {Pierre Ugo Tournoux and J\'er\'emie Leguay and Farid Benbadis and Vania Conan and Marcelo Dias de Amorim and John Whitbeck},
	title = {The Accordion Phenomenon: Analysis, Characterization, and Impact on DTN Routing},
	booktitle = {Proc. {IEEE INFOCOM}},
	year = {2009}
}
 
 2- Not to redistribute the data set to anyone without our permission.
 
 3- Not to use the data for any other purpose than education and research.

 ====
 NB: In order to gain access to this file and the data we provide, you
     should have already confirmed these terms to us by e-mail. If this is
     not already the case, please send us just an e-mail to confirm.

========================
II Data collection and pre-processing: 
========================

We tried to keep the processing of data before public release to a
minimum, to allow any flexibility for possible research use. Some
choices had to be made to reduce power consumption, memory use, and
because of specific capabilities of the iMote prototype. 
Before using these data for your research, it may be important to
check that it does not impact any of your findings.

1- periodic desynchronized scanning.

In our experiment, iMotes were distributed to a group of people to collect
any opportunistic sighting of other Bluetooth devices (including the other
iMotes distributed). Each iMote scans on a periodic basis for devices,
asking them to respond with their MAC address, via the paging function.

It takes approximately 5 to 10s to perform the complete scanning. After
initial tests, we observe that most of the contacts were recorded with a
5s scanning time, and this value was used in the experiment.

The time granularity between two scanning is 15s. It is important to avoid
synchronization of two iMotes around the same cycle clock, as each of them
cannot respond to any request when it is actively scanning. Therefore, we
implemented a random dephasing on [-5s;+5s] to handle this case.

2- skip-length sequence.

A contact "A sees B" is defined as a period of time where all
successive scanning by A receive a positive answer by B. Ideally an
information should be kept at the end of each contact period. 

After preliminary test it became quite clear that a very large number of
contact periods were only separated by one interval. We decided, to avoid
memory overflow, to implement a skip sequence of "one", meaning that a
contact period will only be stopped after two successive failure of a
scanning response. As a consequence, no inter-contact time of less than
two intervals could have been observed.

3- Manual Time synchronization.

Time between iMotes is not synchronized by a central entity, and traces
belonging to different devices bear times which are relative to the
starting time of each device. We recorded the time at which each iMote was
first powered up, which corresponds to time 0 at that iMote. After
collecting the data, we then converted all times into Unix timestamps
(seconds elapsed since 00:00:00 UTC, Jan 1, 1970).

4- Corrupted MAC address, and discarded mote.

As in the Haggle experiments, we observed that a number of MAC addresses
recorded were different from a known one only by one or two digit. They
were most of the time recorded once for a single time slot. It is clear
that at least a part of them comes for a corrupted signal received on the
link level by our devices. We filtered the data set retaining only MAC adresses
of device that have been seen at least twice.


5- Anonymization and Address Identifier.

To protect participants privacy, we choose not to release the MAC address,
neither from the iMotes nor from other external devices recorded. Every
device is given a unique identifier, usually called ID number in this
document. Depending on which number, it might be an iMote or another MAC
address that were recorded from other active Bluetooth devices around.

========================
III iMotes deployment
========================

In the experiment we performed, we were interested in tracking contacts
between different mobile users.

The data set has been collected on August 20, 2006. According to organizers
and police information, about 2,500 people participated to the rollerblading
tour (few rain showers just before the tour resulted in a number of participants
below the average). The total duration of the tour was about three hours,
composed of two sessions of 80 minutes, interspersed with a break of 20 minutes.

During the tour the iMotes has been deployed in three main group of skaters divided as following:
	--Staff members which are themselves organized into six groups: 
		-Front left and front right
		-Rear left and rear right
		-Front and rear. 
		25 iMotes were entrusted among these six groups. These positions are relative and may have not been always respected by the skaters. There are two iMotes that always stayed at their assignated positions, one at the front and one at the back of the tour.
	--Skating associations, which receveid 26 iMotes. This is a group of skilled skaters which were expected to be highly mobile
	--A set of friends which received 11 iMotes. The belonging of each iMote ID to one of these groups is described in part IV

The experiment started on Sunday, 20 Aug 2006 14:24:06 (GMT),
and stopped on Sunday, 20 Aug 2006 17:14:00 (GMT).


========================
IV Description of the files in each experiment
========================

=====
"MAC3Btable.dat"
is a file that contains the three first bytes of the MAC address,
associated with each ID. It could be useful to identify the manufacturer
of each external device.

=====
"contacts.dat"
is a file which describes the contact that were recorded by all
devices we distributed during this experiment.
A contact between two devices A and B is reported only once and last
the time that A sees B or B sees A.

========================
Examples taken from table.Exp1.dat (two first columns and first rows)
========================
51      377     1156089135      1156089164      7       498
51      377     1156089399      1156089399      8       235
51      377     1156089428      1156089428      9       29
51      377     1156089569      1156089585      10      141
51      377     1156090078      1156090078      11      493
51      377     1156090532      1156090532      12      454
51      377     1156090833      1156090833      13      301
51      377     1156090914      1156090914      14      81
51      377     1156090946      1156090966      15      32
51      377     1156093426      1156093426      16      2460
51      377     1156093798      1156093798      17      372
51      381     1156088465      1156088465      1       0
51      389     1156087797      1156087797      1       0
51      396     1156085474      1156085474      1       0
51      396     1156085603      1156085603      2       129
51      396     1156087039      1156087051      3       1436
========================
========================

- The first and second columns gives the IDs of the devices of 
which the contact is reported.

- The third and fourth column describe, respectively, the first and
last time when:
	-the address of ID2 were recorded by ID1
	OR 
	-the adress of ID1 were recorded by ID2 for this contact. 

- The fifth and sixth column are here for reading convenience. The
fifth enumerate contacts with same ID1 and ID2, as 1,2,... . The last
column describes the time difference between the beginning of this
contact and the end of the previous contact with same ID1 and ID2. It
is by convention set to 0 if this is the first contact for this ID1
and ID2.
=====


- Times are unix timestamps which correspond to the number of seconds
since midnight January 1, 1970 UTC (referred to as the Epoch). 

To ease the understanding of data while keeping a sufficent privacy level, 
we provide here the group belonging of iMotes ID:

	-Skaters associations ( skilled skaters ): 
					[1  - 26]
	-Staff:
					[27 - 51]
		-3 Front: 27, 33, 41
		-2 Front left: 29, 42
		-4 Front right: 32, 47, 48, 49
		-5 Rear left: 31, 35, 37, 43, 51
		-3 Rear right: 34, 44, 45
		-6 Rear: 28, 36, 38, 40, 46, 50
		*Nodes 27 and 38 were respectively known to be always at the head and the tail of the roller tour.
		*Nodes 30 and 39 were rescuer, not affected to any particular place.
	-Set of friends: 
					[52 - 62]

The 1050 external devices ( cell phones, PDAs ...) have IDs from 63 to 1112.

========================
IV Answer to some additional questions
========================

- Do you have any location or speed data ?

The answer is no. We did only gather data on the contacts between
mobile devices, that is an indication of their proximity.
In that sense, they may not be considered as classical mobility
traces, focusing on geographical position or speed. 

========================
V Feedback
========================

Feedback on this data is extremely welcomed. Please do not hesitate
to contact one of us if you have any question, or need any extra
information about the experimental settings.

========================
VI Acknowledgements
========================

   We thank James Scott and Pan Hui formerly from Intel
Research Cambridge for the iMotes that they lent to us and for
all the useful discussions. We also thank Timur Friedman and
Bruno Dalouche from UPMC Univ Paris 06 for their support
and technical help while preparing the deployment. Finally,
we are grateful to Philippe Moulie and all the staff members
from Roller & Coquillages.

We would like to Pan Hui, Augustin Chaintreau and 
James Scott for letting us the possibility to adapt their
original README.txt for this iMote experiment.

|=======================================================|
|	Jeremie Leguay <jeremie.leguay@lip6.fr>,	|
|	Farid Benbadis <farid.benbadis@gmail.com>	|
|=======================================================|
