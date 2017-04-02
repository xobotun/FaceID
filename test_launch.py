from Application import Application
import traceback

try:
    app = Application()
except:
    tb = traceback.format_exc()
else:
    tb = "Correct termination"
finally:
    print tb
