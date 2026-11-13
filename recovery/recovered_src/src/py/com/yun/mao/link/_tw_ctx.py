# Recovered module: src.py.com.yun.mao.link._tw_ctx
# Fernet/RSA configuration context reconstructed from the Nuitka constants
# chunk and the runtime TwCtx signature evidence. The encrypted catalog values
# are retained as data; callers can inspect the configuration flow without
# running the original executable.
from __future__ import annotations

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization

from ._fds_jm import sec
from ._jmpz_cy import decrypt_token, is_placeholder_static_key
from ._tw_ceng import (
    assem_rk_a,
    decrypt_with_layer_d,
    tw_sjk_ph,
    unwrap_to_layer_d,
)


class TwCtx:
    _ENC_KEY_B = 'Z0FBQUFBQnFpcFd0UUdPZHpFTlNVX3h5MjFmR1pEeUdIeWZ2S3FQdWNqWVY3VHI4RExvS3gxTE05TFNjc2tjVFFUNE1hVmstemQ0Qnpaa09lQ25JQWdVTkZSZ1VGOFl1U1hsR3hjejVqTW0zNE5ibEo2am1aRmRJcGpvVkxSVVhsSWNnbVFKamFmcnk='
    _ENC_KEY_C = 'Z0FBQUFBQnFpcFd0NzJ6SlRWLWFsMVFHeHZ5VU5XTmRUdDhUNDhyblNZTG9nZ2FXWjF5Nk9qYkVLNmxUdW9BZmF2ZmY4bkxicFFYQ2VMa09adjJPMzhEaklFZUxTVngzcWo0YzFxbnNBYmVWVmQ1Y2JLQW9zV2lRMm1iYUlyVkt6WDJLOU5hclVNSDU='
    _ENC_KEY_D = 'Z0FBQUFBQnFpcFd0THlMV3EwTHBYX1p4Smtmb0lxUUh4SWJqU2lqQ2xKRG44TFVocl9lT0RyeTNaV1dlU19EeEdJVWQ4UWYyWmc2ZEhqWEl1WlpHeHpNbVBOSmN1VHlhRF95SlRPZjhhbmJSX1pxTUJwZnJoN0ZtbHJrWC01eGdpa2dILW5PODJvYXA='
    _ENC_INIT_URL_DEV = 'Z0FBQUFBQnFpcFd0X09Vd2w0Nk9uQ3Z1by1IaW90a0tFTUdHNXVYVGJQT0puaVVpaTJ2U20yMU9oZmFTWktVaUU3a1puMFhFX2N1RWp6SlZaa1J4Z0M2c1pNYWpOTUZHY1BsME5EdzBhRm9zOFk2M0FzWW9BTTA9'
    _ENC_INIT_URL_PROD = 'Z0FBQUFBQnFpcFd0SkwyWEdpTlh1Qzd6dVdhSmttZkwtY2MzV1BlT0EzMDdBN01TZk5lUWhuWXRnTWRlY3FHbUdpS1FzaVJ0LV9hWGFfalh3aFh0d2twdmFwbzVFVlNtQUdEdmd3Y0tsWUJJOUdPekVjYmhRb0xXcE5kWDhGcnpicjlBb2tXY0ZnTms='
    _ENC_INIT_PUBLIC_KEY = 'Z0FBQUFBQnFpcFd0SFBUcW83TG1kNDUzbmpRWFI1QXBmWUY4eEI5a3NQb3F2Ul9zOTJQT05rM2lCUE9yTnVGTDRRNWxOWUlaMzRnNExSR1ZPTDBMWkhpdlJmZ0FsTkdsZ05hb0tqVVZ3ekpsVnY3NkNSZ2lxX0s1NU5GYVBJVExLWmszNXRfN2pzd002NWNoVkY0dUZIV2FqeUVQdS10SXlsbGtTQmtGU0xLX3BNSGZfU0Q1djhGRGEyYVdqS014ZTUxSF91Z0RzcVlPVS1SNHVXeUtNVjQyQlBYZE1RR2psNVQ5QXl2MVp1aXE3WGFGRkJsWGlDMzNMRjVfMlkwaWJWaGNMU2hocU9xdEhWWnYwV2lVcTZwSjFQTHZoTEJDWFBZaEVBa3llQ2o0N1AzVklsQzlfaDQ5bEF3SGJhM2g1NlRJamxvN3FlWU1JdWhCNjdoRlA1RHQ3TFhYN3hLekt1b3YtVVdZckZuQXRBVlBGc1c0eXp6emxfdTRNZzhyLTRtYUVYVjlDeklDT09xRS02R1VYLTJIak1PMGZkSVU5T0Zfdm5hc3NESmRVTjlXWHQwOHc0NU5EZG1Kc0tQd3dlNmhJM2FpYTVISzEyeU80T3V4UktQdU1QTDd0Wk1GZUROMnQxZHJXNGU2eXo5d2FFTGZ2akpsaklWaWpFSnBUQ1NmejctMXVMa2t5T19XYUdubldWMW1fMXpXVU5sMzhvTklpSEQwQzY5V3ZDdG5icDJhYTdVTEg0QmFhb19GdkVXQzlqaFRiblYtdjc4RFRveGJDVjRQWHM3eHBobzlUcHpCdmpiYnludWVvb3ZxVzZyRFZHWl9tUHJvNldhYlVjX1E0RGN3TGhicmY1UDlKMS0wOGFaVzF6VjdHRkktbXgwSVRUYnAwZllDeHViZVlZMms0MUU9'
    _ENCRYPTED_STATIC_KEY = 'Z0FBQUFBQnFpcFd0RFRRc0c1cmgwZXd5UGc2aWVhNEo2bEFrOVNsTXdBR3JxTGxWZmdrQnZZdDRJdUtUODhpNWVEM1ZfSXpkOE5CYUMwdFNaOHpFYjBmYWdFdkd1ZEhTdk1ZcnZNNUhfM1dyLVg3QnZyUVRQZDJFalBnTk5TYWY2eGhpOFZ3aUlWb0g='
    _ENCRYPTED_CONFIGS = {'_p_dh': 'Z0FBQUFBQnFpcFd0NTc4eXBiNUtNaXpWNm1XVTViYUYwRngxX3dQOEY4ODJPVUtrVTlqbk9xTGt4d0JuVGhEZGhTUklNY0xUNHVNMGNjWjQtXzNuczVPa3E5TngxOTFUc3FSX1RJZldGa25ReU1zYWdYSjQ1Xzg9', '_d_lh': 'Z0FBQUFBQnFpcFd0Q0l5UE8wNWM3bFc5bUFreG95eEVNdVpYTHRlSnhyTTRwZlN4Y3J4NXF4OU1Ha0s2bzktMWRzVTRJbDhDeUdESGNBYmNtX1RSVFFWS1dPazN0WEZoTzVFUWpiN2hrdE1RRWdCeWNibEVFQjA9', '_f_pk': 'Z0FBQUFBQnFpcFd0dmhjVkNNMDlWZnQ1VE5ETnNDczM2VEY1ellmcG4yTFRjQXltU0V6cU1xU2IzRmF0MDN5R0N5TlZFZ1FsaEhSZk5ZTUtJY3oxUy15VmJUZFB0aDh2YnliR3pfeURGRC1GVjNDQzhhM2JadVhHRGU5ZkVjd2xNYmdqSXNBMkxQUTNmaXJ4ejRySlFfX0JoSmRpMVl3VTJ3N1dYRHBGSGh1R0FDSXpsemxjTkRMMTBuSlNWVGtSdFJjeXZkdUNwZTJxa0dVLXlaN3p0TUEyTTczcm5WUUU2RG5TQ3d4cEdXYTd2ZXZLcWZGX2RNTkNXOXdqbkVYOEQ1X3VCVkZJdUxFemNQakRISThITkJoMVZ1YnVfemUxXzlRSW5mUkh4Y0pIWVlKaXhVUWJQU0NEOHU3WWRtTmtSRUJ6cnEyeXhRZ1dkanNlUEtkeXFvbVFrQjhQX1A2SWU3LUtnbEt1RWlWYnF4Tm1xcTNJMDZmb2lyWWYwRmIzRE5NUU5sOFNGempmaU5EUU9hZ3o4cmJWQVYyUWplWldsQU9EWnc3TW4zQzNtZy1aRDdTcUpBT19NSTVTQTV4b3RHS0p0MGdUR2dIM0pMNHFPOGpkWExCUml5Q0liS3hYakpOcTZyaDFsYS1sVWl4UFR3M0xwSl9BRGZOS2VKaGZhcW52WlI0dEVjMTFfSUliakM0UGN3ckx4YWxwa3N4NmhJalR0bDFHMlNXUHpMZWhuZVVMZk56blVlcGNaRzJ0RGduNlh5UnNEejhFeW5sSFo2NUFWQ21XZUd4TUJJVEFzX3UxUmlKR0pnOE4xUEw5a0RoZ09fczY3OGZLRTVUN0pYVTJheTJpdmhUY0kxWll4Y2gzRGRnVDlnWkNDNk40WWtNa1ZUQmVVbnRqYkNUM1dMeEZyQnc9', '_r_u': 'Z0FBQUFBQnFpcFd0Nnpfdi1XblNDWHc2ZHJxelNqY3lzd0JTRFc4aDVnZ0g5elZCZDVUR05iTUdnbE95SGcyQVdmR1J2Rl8zYzRCSjZqSHZDWmt5MVV2dVBDdUoyWWpmYWxUR0pVZTZlWnZyOWswS192cy1qQ1Q3MUpMVHpQQTRmOUE4anZSY0poTTg=', '_f_c_u': 'Z0FBQUFBQnFpcFd0TzhxN0ktWHNCWnpIZElLOWtwQkJKZHY4WjgzWmZHWGF0dFJ0VHQyQ1JNaENDNjVNU0kzZlQtRHM2NXRrZEw1MkRiRzFSMUtQNm5OSHBNYXZQRVh4alBBeUNOTUduczhtNklVZDNXOF9Dd1V4ZlA5QWtkYUtJQUp1VTVSUFJ1eWQ=', '_v_uu': 'Z0FBQUFBQnFpcFd0UWJKdjNucEd5OFpWM29Bc0NLRjVtSTZiUDI3dnFKUzRYQlV1YUlPR1RzZVBabTF0dnpGWlk0Szg5bDJ4Q0xtUkp1TkktODh3WjZFVWd4UHpPSDgwQUZuYWJBNG8zeU9ZUTNZY1lBNGxFUDlVUTU2aDNNcFR2eF8yWnFnamU3X1g=', '_r_bu': 'Z0FBQUFBQnFpcFd0NEEyVnBESGxTSTNaU001X3JIcmFnd0FSc2g1TDI3XzZST3B2OXZfSVdrVFlfVWVjeVZRa29qWHJyclFTckY3Sm1HVXlUOE51YU95S0FMWGFlb1hfOVFrN1U3OEVkNWYtOFVSaVdqODRILUU9', '_s_r_u': 'Z0FBQUFBQnFpcFd0ejVVNVJyeHNadHk4WVdScWpjVmI5Y3ozNjRrdW0wYWFfdkNldTJndHRzZS1GeGVZRnktdDNRMEs2N2JQZ0N0VXBueFprUGwxbjdUTzFJc2d2Y205OV80SV9WaHpBSko0ei1pOU5DY3ZRb2o1ZDJZYzVycDNkQ0FuQVUwNFduQ1I=', '_m_cu': 'Z0FBQUFBQnFpcFd0XzVWb24zYWJaRkZtNVdfNzA2d2x2MTBPSkJ6cHg1a0I1ZkIyRHlFNmFHall4bHpWZkFNUHFmNWFxOUprYmxIbzNyTEpLWVZSa084NjRlYm1VM1JKckZWZ0NtZUxRb3JXd2MxN1F3anRJYTJtNExrT2lVcGpQbGI2N3J4UGh5UGo=', '_s_ac_u': 'Z0FBQUFBQnFpcFd0MzBOYWdfZVhNUkY0eEwtQUFNbmc4d01xenJmTGVEQU5EUkJFZElVb2kyTTg5dERCSTZTakdFUG1wdnIxbmY2QVhZeWtIM21sWWtEUV9iTjhOVGdBSVBLVUJScUtLQWVBWEVSMWlLa1NPcXBEQzEzWEZJZHA1TjRhX2t4SHBTUlU=', '_s_co_u': 'Z0FBQUFBQnFpcFd0QUw2am53aXVJaUFkVThPbmpiM3R3MWJKS1BVSkFCYnFhOE9wbGRNM2hBZWJESklTMVNsZHlYT3ctdUI0QmZoMlRrUzdaT2hLZEJ2WHNUd0xGcG1wMlZzNlgtSW1MT3ZScUsxcHJIRjRsVVVWa25IMTFLU2FIRGRidkc4QkxCWTE=', '_s_co_r_u': 'Z0FBQUFBQnFpcFd0TFBhSi05QlA1N01LbXU1X2pUd0hMWFZGNzJPSVY4OU5MV3BhOS1wNHg4bHlQaXdYSGNDYVNfMUxmS1ZUcEpscUZXeDR1YnRaM21mNTM2SjdYbk5MaHNndUg2QVRyZmY1Smk3bjktZklFUW5wNVR0SUk3NWI5MnoyLTJSeGRERFY=', '_s_p_ch_mu': 'Z0FBQUFBQnFpcFd0alJwa2d5SjFLQUllY2JmaUI1dDdtNXhQeExzTEdIUk1UZUVIZVN3bU8zWmRTMUJvQXM4ZEVmQW9iRGVpMkRweDVRdzFPeVR2Y0c1cmpTdTlESmFEU2staFpYQmdFbE9EYy1xNldzYXVKQkM4X1NwRmFlRWVRZ0UxZko2c29zamQ=', '_s_p_co_mu': 'Z0FBQUFBQnFpcFd0NGN4R1hGUGtHV1FvazZrTVY0MEdYTnc5TTdBZk9QMEIwZ3ZQX3MzWENVTmh4dWhIdHZwd2h4Q2ltUWNzNEFjakFHbm8tS3hzRC1uUm5WMmx3eE9FTFYtUks2NnRRM3h1TjJzd0ZPRFNOQVVvTHhHS3hFV1VVM2pxVDhHejcxQmw=', '_r_pk': 'Z0FBQUFBQnFpcFd0d3ZJaDVxbGFkcTJ0enl0dllxUlB3TkYxSHpJaGhNLVB4VkdjWFpMckgxdFlFeFN0aGlxa0x5X29BSkZiZktTVGhpQkN2MjZtZEZYOFIxamZiLWZyTnQzZXhZZ1lTWDlkYmNteDlHSEVVajROUDF5NFoza2hDTWJnUlRxZXIwQXRpcVZ2ckNUQ3dVdTFJdEJIa2tldWIzY2puNThrc2U3T3VZRmhBcGhuSW84QW1sSzFhZmtCY0NSTWJ4N3RYTmQ0WHhQc3E4SzhJZWdEa05qLUd2cGkyNTd5SjVhTF94ZFpDRkY2X29veEZrYzhnTXFveS1GVHdQc0ozanJHSHVlY1FSbnE2TE1nNXB5VmlkWXh3aUtBdEtYMktEVXV3Z1VlR1QtYlVCNW9felA0U1pzS3hXdXhmdjhEVHlPbVlub082QVNiTFpZRkM3QVlRUnZvLVpWSTZzc2pSNUlheDhjM3BudkJ2blhVbDhfMW94YzlSWFo1b3JFNXhZVXJmdXl1ZE5GZlhISHN3VHVWbjJ4ZFExOTBXSHJJZEgxNWJMal9fX0thRWU0RWY0TnE1UjdTNjc0Y251QlZrU2FwVTJJVzhZZmJyQWlTb1ZDVEFNNDY2a1Z5ZTRZVVVxSWw0RWFnWWJNZ2ZsZXRTRmIzMTlxQkJqdkpZNElNUnlUV1hvQ1pJV21zbEJOVkdQdjViYmFUQUsxQkwyR0VRbTZ1MXpwejVEZGFFU0JyejNFb0h5ZXU5NXpud3JrVjl1MUlxdnNHcndUZTRoMDJ5MHhTVmdNNzVRb1VtYnhNZTFDdTBrU1pKM1VNUWZMN0FHTXV1Y2NCTy1hZHBtZW0zTnJaT19oSUpJU0dRMHZfSDFtNF9LZFY5WEFHenhQTnlxLVhTY1lkRzhWOTJjT0JubU09', '_v_p_i_u': 'Z0FBQUFBQnFpcFd0VllrUmxzNnNjVWhFQXdERG9QZ0RoZWdmeXowUzJySGZHMGtmZmtkc2VwakpVVGtjdTEzRS0wc2R5SmtvQ2F1MzNwVEYtNmVLNURDXy1pU2FwVTF1dmc9PQ==', '_v_ps_i_u': 'Z0FBQUFBQnFpcFd0VHA3Z2xBRFNnbjdkeC1MY2w2OTktUF9RLWRmTDhFRGVzSHBrS2FWLXNHWDNBbXk3U3Z1WTR6VnBKa3ZoakMyaDdSSVZxVDg1T0FyZXBKVFZGdFRJX1E9PQ==', '_v_r_p_i_u': 'Z0FBQUFBQnFpcFd0S1RaRU14Z0FKalE4UDcyRDBaUXF3eXNTcnNFbUZldk45Y1ZiMHgxZUw5Sm5Gd05kOWFNcWJWNmw3VGhMU05vYnZIX3phTXAzNjBDTE05Sm4xLUE2NFE9PQ==', '_v_u_i_u': 'Z0FBQUFBQnFpcFd0a0REM3h1dWExV3htMWJfUFR3aURyb1pPbm1YNTdZOWlhdUtiRWxfcmx6TjYyMHJqdzZKcXpLZGUyWXdPaEFWSzBRX1dIVEF2MHBnMGFDWEdoT1pRSWc9PQ==', '_v_s_c_i_u': 'Z0FBQUFBQnFpcFd0dmpqOHU1UXpsbUZEVmt0VHpLNnFkWVZ4bVJRbkpkNDBzSnQzMl82dHFnZ2xwZmR4MkxiNnAyUnNRV0NENTh6VVN4RHhiN0RxMFVzWVlibkFNYjNtT0E9PQ==', '_v_s_f_ms': 'Z0FBQUFBQnFpcFd0cmVUY3dWaVYwSV9GckRZMlNiSWxrckstbHU1SkFCMk8yWnI1Vkdma3FoVEp0c1VLN0dWTlZBdjhDZ0g0UjZCSFBYbXdOVVAzUTR6a3BMTElsVWxCUEE9PQ=='}

    _layer_d: bytes | None = None
    _init_public_key_pem: str | None = None
    _static_cipher: Fernet | None = None
    _root_key: str | None = None

    @classmethod
    def _ensure_built(cls) -> None:
        if cls._static_cipher is not None:
            return
        if tw_sjk_ph(cls._ENC_INIT_URL_DEV) or tw_sjk_ph(cls._ENC_INIT_PUBLIC_KEY):
            raise RuntimeError(sec("pz_not_ready_01"))

        # The outer layer unwraps B/C/D using the compiled layer material.
        cls._layer_d = unwrap_to_layer_d(
            cls._ENC_KEY_B,
            cls._ENC_KEY_C,
            cls._ENC_KEY_D,
            root_a=assem_rk_a(),
        )
        cls._init_public_key_pem = decrypt_with_layer_d(
            cls._ENC_INIT_PUBLIC_KEY,
            cls._layer_d,
        )
        static_key = None
        try:
            static_key = decrypt_with_layer_d(
                cls._ENCRYPTED_STATIC_KEY,
                cls._layer_d,
            )
        except Exception:
            static_key = None
        if static_key is None and cls._root_key:
            candidate = str(cls._root_key)
            if not candidate.startswith("-----BEGIN"):
                try:
                    static_key = decrypt_with_layer_d(
                        cls._ENCRYPTED_STATIC_KEY,
                        candidate.encode("ascii"),
                    )
                except Exception:
                    static_key = None
        cls._static_cipher = (
            Fernet(static_key.encode("ascii")) if static_key else None
        )

    @classmethod
    def _layer_d_bytes(cls) -> bytes:
        cls._ensure_built()
        return cls._layer_d or b""

    @classmethod
    def _open_with_d(cls, ciphertext_b64: str) -> str:
        cls._ensure_built()
        return decrypt_with_layer_d(ciphertext_b64, cls._layer_d_bytes())

    @classmethod
    def tw_sjk_url(cls) -> str:
        cls._ensure_built()
        encrypted = cls._ENC_INIT_URL_DEV
        try:
            from src.py.version_code import is_dev_version

            if not is_dev_version():
                encrypted = cls._ENC_INIT_URL_PROD
        except Exception:
            pass
        return cls._open_with_d(encrypted)

    @classmethod
    def tw_sjk_pk_pem(cls) -> str:
        cls._ensure_built()
        return cls._init_public_key_pem or ""

    @classmethod
    def tw_sjk_pk_ld(cls, pem: str | None = None):
        return serialization.load_pem_public_key(
            (pem or cls.tw_sjk_pk_pem()).encode("utf-8")
        )

    @classmethod
    def tw_yy_mk(cls, root_key: str) -> None:
        cls._root_key = root_key

    @classmethod
    def tw_hq_rk(cls) -> str | None:
        cls._ensure_built()
        return cls._root_key

    @classmethod
    def tw_jm_ok(cls) -> bool:
        if is_placeholder_static_key(cls._ENCRYPTED_STATIC_KEY):
            return False
        try:
            cls._ensure_built()
        except Exception:
            return False
        return cls._static_cipher is not None

    @classmethod
    def _static_cipher_instance(cls) -> Fernet:
        cls._ensure_built()
        return cls._static_cipher  # type: ignore[return-value]

    @classmethod
    def tw_hq_by_k(cls, config_name: str) -> str:
        """Decrypt one entry of the embedded configuration catalog."""
        cls._ensure_built()
        encrypted = cls._ENCRYPTED_CONFIGS[config_name]
        raw = base64.b64decode(encrypted, altchars=b"-_")
        cipher = cls._static_cipher_instance()
        if cipher is None:
            raise RuntimeError(sec("pz_not_ready_01"))
        return cipher.decrypt(raw).decode("utf-8")

    @classmethod
    def tw_jm_str(cls, encrypted: str) -> str:
        return decrypt_token(encrypted, cls._layer_d_bytes())

    @classmethod
    def get(cls, config_name: str) -> str:
        return cls.tw_hq_by_k(config_name)
