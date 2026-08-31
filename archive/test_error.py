import sys
import traceback
try:
    import database as db
    print("Database imported.")
    print("Calling db.get_active_scalpers()...")
    scalpers = db.get_active_scalpers()
    print("Success:", scalpers)
except Exception as e:
    print("ERROR CAUGHT:")
    traceback.print_exc()
