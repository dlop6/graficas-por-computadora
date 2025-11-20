"""
Helper script to validate model loading with the current OpenGL/pygame setup.
It creates a tiny hidden GL context and attempts to load each .obj via Model.
"""

import os
import sys


def main() -> int:
    # Ensure relative paths work regardless of where the script is invoked.
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(repo_dir)

    # Quiet pygame banner and force headless drivers for CI/WSL/PowerShell.
    os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
    os.environ.setdefault("SDL_VIDEODRIVER", "offscreen")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

    try:
        import pygame
        from pygame.locals import DOUBLEBUF, HIDDEN, OPENGL
    except ImportError:
        print("ERROR: pygame no está instalado en este entorno.")
        return 1

    try:
        pygame.init()
        pygame.display.set_mode((64, 64), OPENGL | DOUBLEBUF | HIDDEN)
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: No se pudo crear un contexto OpenGL: {e}")
        return 1

    try:
        from model import Model
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: No se pudo importar Model: {e}")
        try:
            pygame.quit()
        finally:
            return 1

    tasks = [
        ("models/Amaryllis City/OBJ/Amaryllis City.obj", False),
        ("models/bulbasur/Bulbasaur.obj", True),
        ("models/charizard/006 - Charizard/BR_Charizard-Shiny01.obj", True),
        ("models/charizard/006 - Charizard/BR_Charizard.obj", True),
        ("models/charizard/006 - Charizard/Charizard.obj", True),
        ("models/charizard/006 - Charizard/P2_CharizardWP.obj", True),
        ("models/eve/Pokemon XY/Eevee/Eevee.obj", True),
        ("models/pokeball/pokeball.obj", True),
        ("models/umbreon/Umbreon/UmbreonHighPoly.obj", True),
        ("models/umbreon/Umbreon/UmbreonLowPoly.obj", True),
    ]

    results = []
    for path, load_textures in tasks:
        try:
            model = Model(path, load_textures=load_textures)
            results.append(
                (
                    path,
                    "OK",
                    len(model.objFile.vertices),
                    len(model.objFile.faces),
                    len(getattr(model, "submeshes", [])),
                )
            )
        except Exception as e:  # noqa: BLE001
            results.append((path, f"ERROR: {e.__class__.__name__}: {e}", None, None, None))

    for res in results:
        print(res)

    pygame.quit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
