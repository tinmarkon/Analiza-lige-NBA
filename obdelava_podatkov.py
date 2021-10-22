import os
import re


sample_player = re.compile(r'.*?data-stat="player" csk=(?P<Naziv>') ### TODO zaključi statistike igralcev