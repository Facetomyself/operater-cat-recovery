// local variable allocation has failed, the output may be wrong!
// write access to const memory has been detected, the output may be wrong!
_QWORD *__fastcall sub_1406CBAD0(
        __int64 a1,
        __int64 a2,
        __int64 a3,
        __int64 a4,
        _QWORD *a5,
        __int64 a6,
        __int64 a7,
        _QWORD *a8,
        __int64 a9,
        __int64 a10)
{
  __int128 v10; // xmm6
  __int64 v11; // rbx
  __int64 v13; // rax
  __int64 v14; // rdx
  __int64 v15; // rax
  __int64 v16; // rdx
  _QWORD *v17; // rax
  __int64 v18; // rsi
  int v19; // eax
  __int64 v20; // rax
  __int64 v21; // rbp
  __int64 v22; // rax
  _QWORD *v23; // rsi
  __int64 v24; // rax
  bool v25; // zf
  _QWORD *v26; // r12
  _QWORD *v27; // rsi
  _QWORD *v28; // rbp
  int v29; // eax
  _QWORD *v30; // rbx
  __int64 v31; // rax
  __int64 v32; // rdx
  __int64 v33; // rdi
  _QWORD *v34; // rcx
  _QWORD *v35; // rax
  __m128i v36; // xmm6
  _QWORD *v37; // r13
  __int64 v38; // rax
  int v39; // r14d
  __int64 v40; // r12
  _QWORD *v41; // rcx
  __int64 v42; // rax
  __int64 v43; // rdx
  unsigned __int64 v44; // r9
  __int128 v45; // xmm0
  __int64 v46; // rax
  __int64 v47; // rax
  __int64 v48; // rdx
  __int64 v49; // rbx
  _QWORD *v50; // rcx
  __m128i v51; // xmm6
  _QWORD *v52; // rbx
  _QWORD *v53; // r9
  __int64 v55; // rdx
  __int64 v56; // rax
  _QWORD *v57; // r12
  int v58; // eax
  int v59; // r14d
  __int64 v60; // rcx
  _QWORD *v61; // r12
  __int64 v62; // rdx
  __int64 v63; // rax
  _QWORD *v64; // r13
  __int64 v65; // rax
  _QWORD *v66; // r14
  __int64 v67; // rax
  __int64 v68; // rdx
  __int64 v69; // rbx
  _QWORD *v70; // rcx
  __int64 v71; // rax
  __int64 v72; // rdx
  __int64 v73; // rdx
  unsigned __int64 v74; // r8
  __int128 v75; // xmm0
  __int64 v76; // rax
  __int64 v77; // rax
  __int64 v78; // rax
  __int64 v79; // rdx
  unsigned __int64 v80; // r8
  __int128 v81; // xmm0
  __int64 v82; // rax
  __int64 *v83; // rax
  __int64 v84; // rdx
  __int64 v85; // rax
  __int64 v86; // rax
  __int64 v87; // rax
  __int64 v88; // rdx
  __int64 v89; // rdx
  unsigned __int64 v90; // r8
  __int128 v91; // xmm0
  __int64 v92; // rax
  __m128i v93; // xmm0
  __int64 v94; // rax
  __m128i v95; // xmm0
  __m128i v96; // xmm0
  __m128i v97; // xmm0
  _QWORD *v98; // [rsp+B8h] [rbp+20h] BYREF

  *(_OWORD *)&a10 = v10;
  v11 = qword_143943D90;
  a8 = nullptr;
  *(_OWORD *)&a6 = 0;
  if ( qword_143943D90 == 0 )
    goto LABEL_4;
  v13 = *(_QWORD *)qword_143943D90;
  if ( *(__int64 *)qword_143943D90 > 1 )
  {
    *(_QWORD *)qword_143943D90 = v13 - 1;
LABEL_4:
    qword_143943D90 = ((__int64 (__fastcall *)(__int64, __int64, __int64, __int64))unk_142F58E90)(
                        a1,
                        a2: qword_143943FB8,
                        a3: qword_143943E90,
                        a4: 16);
    v11 = qword_143943D90;
    goto LABEL_5;
  }
  if ( *(_QWORD *)(qword_143943D90 + 16) != 0 )
  {
    v38 = v13 - 1;
    *(_QWORD *)qword_143943D90 = v38;
    if ( v38 == 0 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(qword_143943D90 + 8) + 48LL))(a1: qword_143943D90);
    goto LABEL_4;
  }
LABEL_5:
  v14 = *(_QWORD *)(a1 + 56);
  v15 = *(_QWORD *)(v14 + 8);
  *(_QWORD *)(v11 + 120) = v15;
  *(_QWORD *)(v14 + 8) = v11 + 72;
  if ( v15 != 0
    && (*(_BYTE *)(v15 + 69) == 1
     || *(_QWORD *)(v15 + 56) >= (unsigned __int64)(*(_QWORD *)(v15 + 32)
                                                  + 2LL * *(int *)(*(_QWORD *)(v15 + 32) + 168LL)
                                                  + 184)) )
  {
    v16 = *(_QWORD *)(v11 + 112);
    if ( v16 != 0 )
    {
      v17 = *(_QWORD **)(v15 + 40);
      *(_QWORD *)(v16 + 16) = v17;
      if ( v17 != nullptr )
        ++*v17;
    }
  }
  ++*(_QWORD *)v11;
  *(_DWORD *)(v11 + 64) = 0;
  v18 = *(_QWORD *)(qword_14393F5F8 + 32);
  if ( *(_BYTE *)(v18 + 10) != 0 )
  {
    v19 = *(_DWORD *)(v18 + 12);
    if ( v19 == 0 )
    {
      v19 = dword_143547A28;
      *(_DWORD *)(v18 + 12) = dword_143547A28++;
    }
    if ( dword_143547A0C == v19 )
    {
      v20 = qword_143943D88;
      if ( qword_143943D88 < 0 )
        goto LABEL_44;
    }
    else
    {
      dword_143547A0C = v19;
      v20 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
              a1: v18,
              a2: qword_14393F938,
              a3: *(_QWORD *)(qword_14393F938 + 24));
      qword_143943D88 = v20;
      if ( v20 < 0 )
        goto LABEL_44;
    }
    v21 = v18 + (1LL << *(_BYTE *)(v18 + 9)) + 32;
    if ( *(_QWORD *)(v21 + 16 * v20 + 8) != 0 )
      goto LABEL_17;
    v86 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
            a1: v18,
            a2: qword_14393F938,
            a3: *(_QWORD *)(qword_14393F938 + 24));
    qword_143943D88 = v86;
    if ( v86 >= 0 )
    {
      v84 = *(_QWORD *)(v21 + 16 * v86 + 8);
LABEL_119:
      if ( v84 != 0 )
        goto LABEL_17;
    }
  }
  else
  {
    v83 = (__int64 *)MEMORY[0x13B02A410](a1: qword_14393F5F8, a2: qword_14393F938);
    if ( v83 != nullptr )
    {
      v84 = *v83;
      goto LABEL_119;
    }
  }
LABEL_44:
  v35 = (_QWORD *)MEMORY[0x13B02A410](a1: *(_QWORD *)qword_1435FA560, a2: qword_14393F938);
  if ( v35 == nullptr || *v35 == 0 )
  {
    ((void (__fastcall *)(__int64, __int64 *, __int64))unk_142F6E530)(a1, a2: &a6, a3: qword_14393F938);
    v36 = *(__m128i *)&a6;
    v37 = a8;
LABEL_60:
    a8 = v37;
    v39 = 277;
    v28 = nullptr;
    v27 = nullptr;
    *(__m128i *)&a6 = v36;
    goto LABEL_61;
  }
LABEL_17:
  *(_DWORD *)(v11 + 40) = 277;
  v22 = ((__int64 (__fastcall *)(__int64))unk_142F69C20)(a1);
  v23 = (_QWORD *)v22;
  if ( v22 != 0 )
  {
    v24 = MEMORY[0x13B030F90](a1: v22);
    v25 = (*v23)-- == 1;
    v26 = (_QWORD *)v24;
    if ( v25 )
      (*(void (__fastcall **)(_QWORD *))(v23[1] + 48LL))(a1: v23);
    if ( v26 != nullptr )
    {
      v27 = (_QWORD *)(*(__int64 (__fastcall **)(_QWORD *))(v26[1] + 224LL))(a1: v26);
      if ( v27 == nullptr )
      {
        v27 = (_QWORD *)MEMORY[0x13B07F710](a1, a2: &a6, a3: 0, a4: 2);
        if ( v27 == nullptr )
        {
          v28 = nullptr;
LABEL_52:
          v36 = *(__m128i *)&a6;
          v37 = a8;
          a8 = nullptr;
          *(_OWORD *)&a6 = 0;
          v25 = (*v26)-- == 1;
          if ( v25 )
            (*(void (__fastcall **)(_QWORD *))(v26[1] + 48LL))(a1: v26);
          a8 = nullptr;
          *(_OWORD *)&a6 = 0;
          if ( v27 != nullptr )
          {
            v25 = (*v27)-- == 1;
            if ( v25 )
              (*(void (__fastcall **)(_QWORD *))(v27[1] + 48LL))(a1: v27);
          }
          if ( v28 != nullptr )
          {
            v25 = (*v28)-- == 1;
            if ( v25 )
              (*(void (__fastcall **)(_QWORD *))(v28[1] + 48LL))(a1: v28);
          }
          goto LABEL_60;
        }
      }
      v28 = (_QWORD *)(*(__int64 (__fastcall **)(_QWORD *))(v26[1] + 224LL))(a1: v26);
      if ( v28 == nullptr )
      {
        v28 = (_QWORD *)MEMORY[0x13B07F710](a1, a2: &a6, a3: 1, a4: 2);
        if ( v28 == nullptr )
          goto LABEL_52;
      }
      if ( (unsigned __int8)MEMORY[0x13B031120](a1, a2: &a6, a3: v26, a4: 2) == 0 )
        goto LABEL_52;
      v25 = (*v26)-- == 1;
      if ( v25 )
        (*(void (__fastcall **)(_QWORD *))(v26[1] + 48LL))(a1: v26);
      if ( *v27 == 0 )
        (*(void (__fastcall **)(_QWORD *))(v27[1] + 48LL))(a1: v27);
      if ( *v28 == 0 )
        (*(void (__fastcall **)(_QWORD *))(v28[1] + 48LL))(a1: v28);
      v29 = MEMORY[0x13B01B050](a1: v27);
      if ( v29 == -1 )
      {
        v93 = *(__m128i *)(a1 + 96);
        v37 = *(_QWORD **)(a1 + 112);
        v39 = 278;
        *(_QWORD *)(a1 + 112) = 0;
        *(__m128i *)&a6 = v93;
        a8 = v37;
        *(_OWORD *)(a1 + 96) = 0;
        goto LABEL_61;
      }
      if ( v29 != 0 )
      {
        v55 = ((__int64 (*)(void))unk_143219000)();
        if ( v55 == 0 )
        {
          v39 = 280;
          ((void (__fastcall *)(__int64, __int64 *, __int64))unk_142F6E530)(a1, a2: &a6, a3: qword_14393F940);
          v37 = a8;
          goto LABEL_61;
        }
        *(_DWORD *)(v11 + 40) = 280;
        v98 = v27;
        a5 = v28;
        v56 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD **))unk_142F79F60)(a1, a2: v55, a3: &v98);
        v57 = (_QWORD *)v56;
        if ( v56 != 0 )
        {
          v58 = MEMORY[0x13B01B050](a1: v56);
          v25 = (*v57)-- == 1;
          v59 = v58;
          if ( v25 )
            (*(void (__fastcall **)(_QWORD *))(v57[1] + 48LL))(a1: v57);
          if ( v59 != -1 )
          {
            if ( v59 == 0 )
            {
              v87 = *(_QWORD *)(a1 + 16);
              v30 = *(_QWORD **)(v87 + 3616);
              if ( v30 != nullptr )
              {
                v88 = v30[3];
                --*(_DWORD *)(v87 + 3772);
                *(_QWORD *)(v87 + 3616) = v88;
                *v30 = 1;
              }
              else
              {
                v30 = (_QWORD *)((__int64 (__fastcall *)(__int64, __int64))unk_142F54770)(a1: qword_143A35748, a2: 2);
              }
              v89 = *(_QWORD *)(*(_QWORD *)(*(_QWORD *)(qword_143A35A28 + 504) + 16LL) + 744LL);
              v90 = *(_QWORD *)(v89 + 8);
              *(_QWORD *)&v91 = v89;
              v92 = v90 | *(v30 - 1) & 3LL;
              *(_QWORD *)v90 = v30 - 2;
              *((_QWORD *)&v91 + 1) = v92;
              *((_OWORD *)v30 - 1) = v91;
              *(_QWORD *)(v89 + 8) = v30 - 2;
              ++*v27;
              v30[3] = v27;
              ++*v28;
              v30[4] = v28;
              goto LABEL_33;
            }
            v60 = ((__int64 (*)(void))unk_143219FA0)();
            if ( v60 != 0 )
            {
              v61 = (_QWORD *)((__int64 (__fastcall *)(__int64, __int64))unk_1430EC890)(a1: v60, a2: qword_14393F640);
              if ( v61 == nullptr )
              {
LABEL_134:
                v96 = *(__m128i *)(a1 + 96);
                v37 = *(_QWORD **)(a1 + 112);
                v39 = 282;
                *(_QWORD *)(a1 + 112) = 0;
                *(__m128i *)&a6 = v96;
                a8 = v37;
                *(_OWORD *)(a1 + 96) = 0;
                goto LABEL_61;
              }
              v62 = ((__int64 (*)(void))unk_14321A0D0)();
              if ( v62 != 0 )
              {
                *(_DWORD *)(v11 + 40) = 282;
                v63 = ((__int64 (__fastcall *)(__int64, __int64))unk_142F69C20)(a1, a2: v62);
                v64 = (_QWORD *)v63;
                if ( v63 != 0 )
                {
                  *(_DWORD *)(v11 + 40) = 282;
                  v65 = ((__int64 (__fastcall *)(__int64, _QWORD *, __int64))unk_142F6A9F0)(a1, a2: v61, a3: v63);
                  v25 = (*v61)-- == 1;
                  v66 = (_QWORD *)v65;
                  if ( v25 )
                    (*(void (__fastcall **)(_QWORD *))(v61[1] + 48LL))(a1: v61);
                  v25 = (*v64)-- == 1;
                  if ( v25 )
                    (*(void (__fastcall **)(_QWORD *))(v64[1] + 48LL))(a1: v64);
                  if ( v66 != nullptr )
                  {
                    v25 = (*v66)-- == 1;
                    if ( v25 )
                      (*(void (__fastcall **)(_QWORD *))(v66[1] + 48LL))(a1: v66);
                    v67 = *(_QWORD *)(a1 + 56);
                    v68 = *(_QWORD *)(v67 + 8);
                    v69 = *(_QWORD *)(v68 + 40);
                    v70 = *(_QWORD **)(v69 + 16);
                    *(_QWORD *)(v67 + 8) = *(_QWORD *)(v68 + 48);
                    *(_DWORD *)(v69 + 64) = -1;
                    if ( v70 != nullptr )
                    {
                      *(_QWORD *)(v69 + 16) = 0;
                      v25 = (*v70)-- == 1;
                      if ( v25 )
                        (*(void (**)(void))(v70[1] + 48LL))();
                    }
                    v25 = (*(_QWORD *)v69)-- == 1;
                    if ( v25 )
                      (*(void (__fastcall **)(__int64))(*(_QWORD *)(v69 + 8) + 48LL))(a1: v69);
                    v71 = *(_QWORD *)(a1 + 16);
                    *(_QWORD *)(v69 + 120) = 0;
                    v30 = *(_QWORD **)(v71 + 3616);
                    if ( v30 != nullptr )
                    {
                      v72 = v30[3];
                      --*(_DWORD *)(v71 + 3772);
                      *(_QWORD *)(v71 + 3616) = v72;
                      *v30 = 1;
                    }
                    else
                    {
                      v30 = (_QWORD *)((__int64 (__fastcall *)(__int64, __int64))unk_142F54770)(
                                        a1: qword_143A35748,
                                        a2: 2);
                    }
                    v73 = *(_QWORD *)(*(_QWORD *)(*(_QWORD *)(qword_143A35A28 + 504) + 16LL) + 744LL);
                    v74 = *(_QWORD *)(v73 + 8);
                    *(_QWORD *)&v75 = v73;
                    v76 = v74 | *(v30 - 1) & 3LL;
                    *(_QWORD *)v74 = v30 - 2;
                    *((_QWORD *)&v75 + 1) = v76;
                    *((_OWORD *)v30 - 1) = v75;
                    *(_QWORD *)(v73 + 8) = v30 - 2;
                    ++*v27;
                    v30[3] = v27;
                    ++*v28;
                    v30[4] = v28;
                    goto LABEL_39;
                  }
                  goto LABEL_134;
                }
                v97 = *(__m128i *)(a1 + 96);
                v37 = *(_QWORD **)(a1 + 112);
                v39 = 282;
                *(_QWORD *)(a1 + 112) = 0;
                *(__m128i *)&a6 = v97;
                a8 = v37;
                *(_OWORD *)(a1 + 96) = 0;
                v25 = (*v61)-- == 1;
                if ( v25 )
                {
                  (*(void (__fastcall **)(_QWORD *))(v61[1] + 48LL))(a1: v61);
                  v37 = a8;
                }
              }
              else
              {
                ((void (__fastcall *)(__int64, __int64 *, __int64))unk_142F6E530)(a1, a2: &a6, a3: qword_14393F630);
                v25 = (*v61)-- == 1;
                if ( v25 )
                {
                  v39 = 282;
                  (*(void (__fastcall **)(_QWORD *))(v61[1] + 48LL))(a1: v61);
                  v37 = a8;
                }
                else
                {
                  v37 = a8;
                  v39 = 282;
                }
              }
            }
            else
            {
              v39 = 282;
              ((void (__fastcall *)(__int64, __int64 *, __int64))unk_142F6E530)(a1, a2: &a6, a3: qword_14393F638);
              v37 = a8;
            }
LABEL_61:
            if ( v37 != nullptr )
            {
              if ( v37[3] == v11 )
              {
LABEL_69:
                ((void (__fastcall *)(__int64, void *, _QWORD *, _QWORD *))unk_142F544C0)(
                  a1: v11,
                  a2: &unk_14359FC67,
                  a3: v27,
                  a4: v28);
                if ( qword_143943D90 == v11 )
                {
                  v25 = (*(_QWORD *)v11)-- == 1;
                  if ( v25 )
                    (*(void (__fastcall **)(__int64))(*(_QWORD *)(v11 + 8) + 48LL))(a1: v11);
                  qword_143943D90 = 0;
                }
                v47 = *(_QWORD *)(a1 + 56);
                v48 = *(_QWORD *)(v47 + 8);
                v49 = *(_QWORD *)(v48 + 40);
                v50 = *(_QWORD **)(v49 + 16);
                *(_QWORD *)(v47 + 8) = *(_QWORD *)(v48 + 48);
                *(_DWORD *)(v49 + 64) = -1;
                if ( v50 != nullptr )
                {
                  *(_QWORD *)(v49 + 16) = 0;
                  v25 = (*v50)-- == 1;
                  if ( v25 )
                    (*(void (**)(void))(v50[1] + 48LL))();
                }
                v25 = (*(_QWORD *)v49)-- == 1;
                if ( v25 )
                  (*(void (__fastcall **)(__int64))(*(_QWORD *)(v49 + 8) + 48LL))(a1: v49);
                v51 = *(__m128i *)&a6;
                *(_QWORD *)(v49 + 120) = 0;
                *(_OWORD *)&a6 = 0;
                v52 = a8;
                a8 = nullptr;
                if ( v27 != nullptr )
                {
                  v25 = (*v27)-- == 1;
                  if ( v25 )
                    (*(void (__fastcall **)(_QWORD *))(v27[1] + 48LL))(a1: v27);
                }
                if ( v28 != nullptr )
                {
                  v25 = (*v28)-- == 1;
                  if ( v25 )
                    (*(void (__fastcall **)(_QWORD *))(v28[1] + 48LL))(a1: v28);
                }
                v53 = v52;
                a8 = v52;
                v30 = nullptr;
                *(__m128i *)&a6 = v51;
                MEMORY[0x13B00DF80](a1, a2: v51.m128i_i64[0], a3: v51.m128i_i64[1], a4: v53);
                return v30;
              }
              v40 = *(_QWORD *)qword_1435FA6C0;
              if ( *(_QWORD *)qword_1435FA6C0 != 0 )
              {
                v41 = v37;
                *(_QWORD *)qword_1435FA6C0 = *(_QWORD *)v40;
                *(_QWORD *)v40 = 1;
                --*(_DWORD *)qword_1435FA6D0;
              }
              else
              {
                v85 = MEMORY[0x13B00DD60](a1: qword_143A35A88);
                v41 = a8;
                v40 = v85;
              }
              *(_QWORD *)(v40 + 24) = v11;
              ++*(_QWORD *)v11;
              v42 = *(_QWORD *)(qword_143A35A28 + 504);
              *(_DWORD *)(v40 + 36) = v39;
              *(_DWORD *)(v40 + 32) = -1;
              v43 = *(_QWORD *)(*(_QWORD *)(v42 + 16) + 744LL);
              v44 = *(_QWORD *)(v43 + 8);
              *(_QWORD *)&v45 = v43;
              v46 = v44 | *(_QWORD *)(v40 - 8) & 3LL;
              *(_QWORD *)v44 = v40 - 16;
              *((_QWORD *)&v45 + 1) = v46;
              *(_OWORD *)(v40 - 16) = v45;
              *(_QWORD *)(v43 + 8) = v40 - 16;
              *(_QWORD *)(v40 + 16) = v37;
              ++*v37;
              if ( v41 != nullptr )
              {
                v25 = (*v41)-- == 1;
                if ( v25 )
                  (*(void (**)(void))(v41[1] + 48LL))();
              }
            }
            else
            {
              v40 = *(_QWORD *)qword_1435FA6C0;
              if ( *(_QWORD *)qword_1435FA6C0 != 0 )
              {
                *(_QWORD *)qword_1435FA6C0 = *(_QWORD *)v40;
                *(_QWORD *)v40 = 1;
                --*(_DWORD *)qword_1435FA6D0;
              }
              else
              {
                v94 = MEMORY[0x13B00DD60](a1: qword_143A35A88);
                v37 = a8;
                v40 = v94;
              }
              *(_QWORD *)(v40 + 24) = v11;
              *(_QWORD *)(v40 + 16) = 0;
              ++*(_QWORD *)v11;
              v77 = *(_QWORD *)(qword_143A35A28 + 504);
              *(_DWORD *)(v40 + 32) = -1;
              v78 = *(_QWORD *)(v77 + 16);
              *(_DWORD *)(v40 + 36) = v39;
              v79 = *(_QWORD *)(v78 + 744);
              v80 = *(_QWORD *)(v79 + 8);
              *(_QWORD *)&v81 = v79;
              v82 = v80 | *(_QWORD *)(v40 - 8) & 3LL;
              *(_QWORD *)v80 = v40 - 16;
              *((_QWORD *)&v81 + 1) = v82;
              *(_OWORD *)(v40 - 16) = v81;
              *(_QWORD *)(v79 + 8) = v40 - 16;
              if ( v37 != nullptr )
              {
                v25 = (*v37)-- == 1;
                if ( v25 )
                  (*(void (__fastcall **)(_QWORD *))(v37[1] + 48LL))(a1: v37);
              }
            }
            a8 = (_QWORD *)v40;
            goto LABEL_69;
          }
        }
        v95 = *(__m128i *)(a1 + 96);
        v37 = *(_QWORD **)(a1 + 112);
        v39 = 280;
        *(_QWORD *)(a1 + 112) = 0;
        *(__m128i *)&a6 = v95;
        a8 = v37;
        *(_OWORD *)(a1 + 96) = 0;
        goto LABEL_61;
      }
      v30 = (_QWORD *)qword_14393F880;
      ++*(_QWORD *)qword_14393F880;
LABEL_33:
      v31 = *(_QWORD *)(a1 + 56);
      v32 = *(_QWORD *)(v31 + 8);
      v33 = *(_QWORD *)(v32 + 40);
      v34 = *(_QWORD **)(v33 + 16);
      *(_QWORD *)(v31 + 8) = *(_QWORD *)(v32 + 48);
      *(_DWORD *)(v33 + 64) = -1;
      if ( v34 != nullptr )
      {
        *(_QWORD *)(v33 + 16) = 0;
        v25 = (*v34)-- == 1;
        if ( v25 )
          (*(void (**)(void))(v34[1] + 48LL))();
      }
      v25 = (*(_QWORD *)v33)-- == 1;
      if ( v25 )
        (*(void (__fastcall **)(__int64))(*(_QWORD *)(v33 + 8) + 48LL))(a1: v33);
      *(_QWORD *)(v33 + 120) = 0;
LABEL_39:
      v25 = (*v27)-- == 1;
      if ( v25 )
        (*(void (__fastcall **)(_QWORD *))(v27[1] + 48LL))(a1: v27);
      v25 = (*v28)-- == 1;
      if ( v25 )
        (*(void (__fastcall **)(_QWORD *))(v28[1] + 48LL))(a1: v28);
      return v30;
    }
  }
  v36 = *(__m128i *)(a1 + 96);
  v37 = *(_QWORD **)(a1 + 112);
  *(_QWORD *)(a1 + 112) = 0;
  *(_OWORD *)(a1 + 96) = 0;
  goto LABEL_60;
}