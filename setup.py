from cx_Freeze import setup, Executable

setup(
    name="GetMarks",
    version="1.0",
    description="description",
    executables=[Executable("main.py")],
    options={
        'build_exe': {
            'includes': ['pandas', 'random', 'os', "requests", "threading","bs4", "datetime", "csv"],
        },
    },
)
