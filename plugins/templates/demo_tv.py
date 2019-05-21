from dramatica.templates import DramaticaTemplate
from dramatica.timeutils import *

__manifest__ = {
    "name"        : "DEMO TV",
    "description" : "Dramatica demo channel schedule",
    "author"      : "martas@imm.cz"
}



class Template(DramaticaTemplate):
    def apply(self):

        MAIN_GENRES = {
            MON : ["horror"], 
            TUE : ["political", "social", "conspiracy"],
            WED : ["arts"],
            THU : ["technology"],
            FRI : ["rock"],
            SAT : ["rock"],
            SUN : ["drama", "comedy"]
        }[self.dow]


        JINGLE_FEED = {
            MON : "path like '%horror_%'",
            TUE : "path like '%paranoia_%'",
            WED : "path like '%art_%'",
            THU : "path like '%tech_%'",
            FRI : "path like '%generic_%'",
            SAT : "path like '%generic_%'",
            SUN : "path like '%generic_%'"
        }[self.dow]


        self.add_block("06:00", title="Morning mourning")
        self.configure(
            solver="Default", 
            genres=["Pop", "Rock", "Alt rock"],
            target_duration=dur("04:00:00"),
            solve_empty=True,
            run_mode=2
            )

        self.add_block("10:00", title="Some movie")
        self.configure(
            solver="MovieBlock",
            run_mode=2,
            target_duration=dur("02:30:00"),
            genres=["movie"],
            )   

        self.add_block("12:30", title="Rocking")
        self.configure(
            solver="MusicBlock",
            genres=["Rock"],
            intro_jingle="path LIKE '%vedci_zjistili%'",
            jingles="path LIKE '%vedci_zjistili%'"
            )   

        self.add_block("15:00", title="Another movie")
        self.configure(
            solver="MovieBlock",
            genres=MAIN_GENRES
            )   

        self.add_block("19:00", title="PostX")
        self.configure(
            solver="MusicBlock",
            genres=["Alt rock"],
            intro_jingle="path LIKE '%postx_short%'",
            outro_jingle="path LIKE '%postx_short%'",
            jingles="path LIKE '%postx_short%'"
            )   

        self.add_block("21:00", title="Movie of the day")
        self.configure(
            solver="MovieBlock",
            genres=MAIN_GENRES
            )   

        self.add_block("23:00", title="Nachtmetal")
        self.configure(
            solver="MusicBlock",
            genres=["Metal"],
            intro_jingle="path LIKE '%nachtmetal_intro%'",
            jingles="path LIKE '%nachtmetal_short%'",
            target_duration=dur("02:00:00"),
            )   
