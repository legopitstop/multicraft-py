from multicraft.contrib.app import MulticraftDesktop
from multicraft import BISECT_PREMIUM
import dotenv

dotenv.load_dotenv()

if __name__ == "__main__":
    # pass MULTICRAFT_USER instead of user
    app = MulticraftDesktop(BISECT_PREMIUM, "legopitstop", 141815)
    app.mainloop()
