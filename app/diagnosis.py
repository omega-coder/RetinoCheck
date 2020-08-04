class DRDiagnosis(object):
    def __init__(self):
        self.DIAG = {
            0: {"stade": "Oeil Sain", "description": "Pas de Maladie!", "uistyle": "card-0"},
            1: {
                "stade": "Mild Nonproliferative DR",
                "description": "It means that there are tiny bulges in the tiny blood vessels in your retinas. The bulges are called microaneurysms. They may cause the vessels to leak small amounts of blood into your retinas. At this early stage, you probably don't have vision problems, so you may not need treatment.",
                "uistyle": "card-1",
            },
            2: {
                "stade": "Moderate Nonproliferative DR",
                "description": "also called pre-proliferative retinopathy. At this stage, the blood vessels in your retinas swell. They may not carry blood as well as they used to. These things can cause physical changes to the retina.",
                "uistyle": "card-2",
            },
            3: {
                "stade": "Severe Nonproliferative DR",
                "description": "In this stage, your blood vessels become even more blocked. This means even less blood goes to the retinas. Because of this, scar tissue forms. The lack of blood triggers a signal to your retinas to create new blood vessels.",
                "uistyle": "card-3",
            },
            4: {
                "stade": "Proliferative DR",
                "description": "In this advanced stage, new blood vessels grow in your retinas and into the gel-like fluid that fills your eyes. This growth is called neovascularization. These vessels are thin and weak. They often bleed. The bleeding can cause scar tissue",
                "uistyle": "card-4",
            },
        }

    def get(self, index, type_info):
        return self.DIAG[index][type_info]

    def change_info(self, index, type_info, desired_text):
        self.DIAG[index][type_info] = desired_text
