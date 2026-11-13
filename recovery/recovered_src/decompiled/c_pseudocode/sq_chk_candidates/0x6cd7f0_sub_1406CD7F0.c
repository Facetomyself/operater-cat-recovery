// local variable allocation has failed, the output may be wrong!
// write access to const memory has been detected, the output may be wrong!
__int64 __fastcall sub_1406CD7F0(
        _QWORD *a1,
        __int64 a2,
        __int64 a3,
        __int64 a4,
        __int64 a5,
        _QWORD *a6,
        __int64 a7,
        _QWORD *a8,
        __int64 a9,
        __int64 a10,
        _QWORD *a11,
        _QWORD *a12)
{
  __int64 v12; // rbx
  __int64 v14; // rax
  __int64 v15; // rdx
  __int64 v16; // rax
  __int64 v17; // rdx
  _QWORD *v18; // rax
  __int64 v19; // rcx
  int v20; // eax
  __int64 v21; // r8
  __int64 v22; // rdi
  int v23; // eax
  __int64 v24; // rax
  __int64 v25; // rbp
  _QWORD *v26; // rdi
  __int64 v27; // rax
  bool v28; // zf
  _QWORD *v29; // rbp
  __int64 v30; // rax
  __int64 v31; // rdi
  _QWORD *v32; // r14
  __m128i v33; // xmm0
  _QWORD *v34; // r12
  __int64 *v35; // rbp
  _QWORD *v36; // rdi
  _QWORD *v37; // rcx
  __int64 v38; // r13
  __int64 v39; // rdx
  unsigned __int64 v40; // r9
  __int128 v41; // xmm0
  __int64 v42; // rax
  __int64 v43; // rax
  _QWORD *v44; // rcx
  _QWORD *v45; // rcx
  _QWORD *v46; // rcx
  _QWORD *v47; // rcx
  _QWORD *v48; // r15
  __int64 v49; // rdi
  int v50; // eax
  __int64 v51; // r14
  __int64 v52; // rax
  __int64 v53; // rdx
  __int64 v54; // r15
  __int64 v55; // r14
  __int64 v56; // rdx
  int v57; // r12d
  __int64 v58; // rcx
  __int64 v59; // rax
  __int64 v60; // rdx
  __int64 v61; // rbx
  _QWORD *v62; // rcx
  __int64 v64; // rax
  _QWORD *v65; // rax
  _QWORD *v66; // r15
  __int64 v67; // rax
  _QWORD *v68; // rcx
  _QWORD *v69; // r14
  _QWORD *v70; // rdi
  __int64 v71; // rcx
  __int64 v72; // rax
  _QWORD *v73; // rcx
  __int64 v74; // rax
  int v75; // edx
  __int64 v76; // rdx
  __int64 v77; // rcx
  __int64 v78; // rax
  __int64 v79; // rdi
  __int64 v80; // rax
  __int64 v81; // rax
  __int64 v82; // rcx
  unsigned __int64 v83; // r9
  __int128 v84; // xmm0
  __int64 v85; // rax
  __int64 v86; // rax
  __int64 v87; // rdx
  __int64 v88; // rbx
  _QWORD *v89; // rcx
  __int64 v90; // r9
  int v91; // r12d
  __int64 v92; // rdx
  unsigned __int64 v93; // r8
  __int128 v94; // xmm0
  __int64 v95; // rax
  _QWORD *v96; // rcx
  __int64 v97; // rax
  __int64 v98; // rax
  __int64 v99; // rdx
  unsigned __int64 v100; // r8
  __int128 v101; // xmm0
  __int64 v102; // rax
  __int64 *v103; // rax
  __int64 v104; // rdx
  __int64 v105; // rax
  __int64 v106; // rax
  int v107; // eax
  __int64 v108; // rax
  __int64 v109; // rax
  __int64 v110; // rax
  __int64 v111; // [rsp+D8h] [rbp+20h]
  __int64 v112; // [rsp+D8h] [rbp+20h]
  __int64 v113; // [rsp+D8h] [rbp+20h]
  __int64 v114; // [rsp+D8h] [rbp+20h]

  v12 = qword_143943D28;
  if ( qword_143943D28 == 0 )
    goto LABEL_4;
  v14 = *(_QWORD *)qword_143943D28;
  if ( *(__int64 *)qword_143943D28 > 1 )
  {
    *(_QWORD *)qword_143943D28 = v14 - 1;
LABEL_4:
    qword_143943D28 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64, _QWORD))unk_142F58E90)(
                        a1,
                        a2: qword_143943F38,
                        a3: qword_143943E90,
                        a4: 0);
    v12 = qword_143943D28;
    goto LABEL_5;
  }
  if ( *(_QWORD *)(qword_143943D28 + 16) != 0 )
  {
    v64 = v14 - 1;
    *(_QWORD *)qword_143943D28 = v64;
    if ( v64 == 0 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(qword_143943D28 + 8) + 48LL))(a1: qword_143943D28);
    goto LABEL_4;
  }
LABEL_5:
  v15 = a1[7];
  v16 = *(_QWORD *)(v15 + 8);
  *(_QWORD *)(v12 + 120) = v16;
  *(_QWORD *)(v15 + 8) = v12 + 72;
  if ( v16 != 0
    && (*(_BYTE *)(v16 + 69) == 1
     || *(_QWORD *)(v16 + 56) >= (unsigned __int64)(*(_QWORD *)(v16 + 32)
                                                  + 2LL * *(int *)(*(_QWORD *)(v16 + 32) + 168LL)
                                                  + 184)) )
  {
    v17 = *(_QWORD *)(v12 + 112);
    if ( v17 != 0 )
    {
      v18 = *(_QWORD **)(v16 + 40);
      *(_QWORD *)(v17 + 16) = v18;
      if ( v18 != nullptr )
        ++*v18;
    }
  }
  ++*(_QWORD *)v12;
  *(_DWORD *)(v12 + 64) = 0;
  v19 = ((__int64 (*)(void))unk_143218D60)();
  if ( v19 == 0 )
  {
    ((void (__fastcall *)(_QWORD *, __int64 *, __int64))unk_142F6E530)(a1, a2: &a10, a3: qword_14393F948);
    v56 = (__int64)a12;
    v55 = a10;
    v48 = a11;
    if ( a12 == nullptr )
    {
LABEL_132:
      v35 = (__int64 *)qword_1435FA6C0;
      v38 = qword_143A35A28;
      v91 = 342;
      goto LABEL_146;
    }
LABEL_112:
    if ( *(_QWORD *)(v56 + 24) != v12 )
    {
      v35 = (__int64 *)qword_1435FA6C0;
      v38 = qword_143A35A28;
      v57 = 342;
      goto LABEL_114;
    }
    goto LABEL_130;
  }
  v20 = MEMORY[0x13B01B050](a1: v19);
  if ( v20 == -1 )
  {
    v56 = a1[14];
    v55 = a1[12];
    a1[14] = 0;
    v48 = (_QWORD *)a1[13];
    *((_OWORD *)a1 + 6) = 0;
    if ( v56 == 0 )
      goto LABEL_132;
    goto LABEL_112;
  }
  if ( v20 != 0 )
  {
    v22 = *(_QWORD *)(qword_14393F5F8 + 32);
    if ( *(_BYTE *)(v22 + 10) != 0 )
    {
      v23 = *(_DWORD *)(v22 + 12);
      if ( v23 == 0 )
      {
        v23 = dword_143547A28;
        *(_DWORD *)(v22 + 12) = dword_143547A28++;
      }
      if ( dword_1435479F4 == v23 )
      {
        v24 = qword_143943D20;
        if ( qword_143943D20 < 0 )
          goto LABEL_84;
      }
      else
      {
        dword_1435479F4 = v23;
        v24 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
                a1: v22,
                a2: qword_14393F9A0,
                a3: *(_QWORD *)(qword_14393F9A0 + 24));
        qword_143943D20 = v24;
        if ( v24 < 0 )
          goto LABEL_84;
      }
      v25 = v22 + (1LL << *(_BYTE *)(v22 + 9)) + 32;
      if ( *(_QWORD *)(v25 + 16 * v24 + 8) != 0 )
        goto LABEL_20;
      v108 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
               a1: v22,
               a2: qword_14393F9A0,
               a3: *(_QWORD *)(qword_14393F9A0 + 24));
      qword_143943D20 = v108;
      if ( v108 >= 0 )
      {
        v104 = *(_QWORD *)(v25 + 16 * v108 + 8);
LABEL_166:
        if ( v104 != 0 )
          goto LABEL_20;
      }
    }
    else
    {
      v103 = (__int64 *)MEMORY[0x13B02A410](a1: qword_14393F5F8, a2: qword_14393F9A0);
      if ( v103 != nullptr )
      {
        v104 = *v103;
        goto LABEL_166;
      }
    }
LABEL_84:
    v65 = (_QWORD *)MEMORY[0x13B02A410](a1: *(_QWORD *)qword_1435FA560, a2: qword_14393F9A0);
    if ( v65 == nullptr || *v65 == 0 )
    {
      ((void (__fastcall *)(_QWORD *, __int64 *, __int64))unk_142F6E530)(a1, a2: &a10, a3: qword_14393F9A0);
      v33 = *(__m128i *)&a10;
      v32 = a12;
      goto LABEL_28;
    }
LABEL_20:
    *(_DWORD *)(v12 + 40) = 344;
    v26 = (_QWORD *)((__int64 (__fastcall *)(_QWORD *))unk_142F69C20)(a1);
    if ( v26 != nullptr )
    {
      v27 = MEMORY[0x13B0312D0](a1, a2: v26, a3: *(_QWORD *)(qword_1435FA6E0 + 16), a4: 0);
      v28 = (*v26)-- == 1;
      v29 = (_QWORD *)v27;
      if ( v28 )
        (*(void (__fastcall **)(_QWORD *))(v26[1] + 48LL))(a1: v26);
      if ( v29 != nullptr )
      {
        v30 = ((__int64 (__fastcall *)(_QWORD *, __int64))unk_1430EC890)(a1: v29, a2: qword_14393F998);
        v28 = (*v29)-- == 1;
        v31 = v30;
        if ( v28 )
          (*(void (__fastcall **)(_QWORD *))(v29[1] + 48LL))(a1: v29);
        if ( v31 != 0 )
          goto LABEL_73;
      }
    }
    v32 = (_QWORD *)a1[14];
    a1[14] = 0;
    v33 = *((__m128i *)a1 + 6);
    *((_OWORD *)a1 + 6) = 0;
LABEL_28:
    v34 = (_QWORD *)a1[39];
    a8 = v32;
    *(__m128i *)&a6 = v33;
    if ( v34 != nullptr )
      ++*v34;
    v35 = (__int64 *)qword_1435FA6C0;
    v36 = *(_QWORD **)qword_1435FA6C0;
    if ( v32 != nullptr )
    {
      if ( v36 != nullptr )
      {
        v37 = v32;
        *(_QWORD *)qword_1435FA6C0 = *v36;
        *v36 = 1;
        --*(_DWORD *)qword_1435FA6D0;
      }
      else
      {
        v105 = MEMORY[0x13B00DD60](a1: qword_143A35A88);
        v37 = a8;
        v36 = (_QWORD *)v105;
      }
      v38 = qword_143A35A28;
      v36[3] = v12;
      ++*(_QWORD *)v12;
      v36[4] = qword_1435A0590;
      v39 = *(_QWORD *)(*(_QWORD *)(*(_QWORD *)(qword_143A35A28 + 504) + 16LL) + 744LL);
      v40 = *(_QWORD *)(v39 + 8);
      *(_QWORD *)&v41 = v39;
      v42 = v40 | *(v36 - 1) & 3LL;
      *(_QWORD *)v40 = v36 - 2;
      *((_QWORD *)&v41 + 1) = v42;
      *((_OWORD *)v36 - 1) = v41;
      *(_QWORD *)(v39 + 8) = v36 - 2;
      v36[2] = v32;
      ++*v32;
      if ( v37 != nullptr )
      {
        v28 = (*v37)-- == 1;
        if ( v28 )
          (*(void (**)(void))(v37[1] + 48LL))();
      }
    }
    else
    {
      if ( v36 != nullptr )
      {
        *(_QWORD *)qword_1435FA6C0 = *v36;
        *v36 = 1;
        --*(_DWORD *)qword_1435FA6D0;
      }
      else
      {
        v110 = MEMORY[0x13B00DD60](a1: qword_143A35A88);
        v32 = a8;
        v36 = (_QWORD *)v110;
      }
      v38 = qword_143A35A28;
      v36[3] = v12;
      v36[2] = 0;
      ++*(_QWORD *)v12;
      v36[4] = qword_1435A0590;
      v92 = *(_QWORD *)(*(_QWORD *)(*(_QWORD *)(qword_143A35A28 + 504) + 16LL) + 744LL);
      v93 = *(_QWORD *)(v92 + 8);
      *(_QWORD *)&v94 = v92;
      v95 = v93 | *(v36 - 1) & 3LL;
      *(_QWORD *)v93 = v36 - 2;
      *((_QWORD *)&v94 + 1) = v95;
      *((_OWORD *)v36 - 1) = v94;
      *(_QWORD *)(v92 + 8) = v36 - 2;
      if ( v32 != nullptr )
      {
        v28 = (*v32)-- == 1;
        if ( v28 )
          (*(void (__fastcall **)(_QWORD *))(v32[1] + 48LL))(a1: v32);
      }
    }
    a8 = v36;
    if ( a6 != (_QWORD *)qword_143A35618 && a6 != nullptr )
    {
      ((void (__fastcall *)(_QWORD *, _QWORD **, __int64 *, _QWORD **))unk_142FAD280)(a1, a2: &a6, a3: &a7, a4: &a8);
      v36 = a8;
    }
    v43 = a7;
    v44 = *(_QWORD **)(a7 + 40);
    if ( v36 == (_QWORD *)qword_143A35618 )
    {
      v36 = nullptr;
    }
    else if ( v36 != nullptr )
    {
      ++*v36;
    }
    *(_QWORD *)(v43 + 40) = v36;
    if ( v44 != nullptr )
    {
      v28 = (*v44)-- == 1;
      if ( v28 )
      {
        (*(void (**)(void))(v44[1] + 48LL))();
        v43 = a7;
      }
    }
    v45 = (_QWORD *)a1[39];
    a1[39] = v43;
    if ( v45 != nullptr )
    {
      v28 = (*v45)-- == 1;
      if ( v28 )
        (*(void (**)(void))(v45[1] + 48LL))();
    }
    v46 = a6;
    v28 = (*a6)-- == 1;
    if ( v28 )
      (*(void (**)(void))(v46[1] + 48LL))();
    v47 = a8;
    if ( a8 != nullptr )
    {
      v28 = (*a8)-- == 1;
      if ( v28 )
        (*(void (**)(void))(v47[1] + 48LL))();
    }
    v48 = (_QWORD *)a1[39];
    a8 = nullptr;
    *(_OWORD *)&a6 = 0;
    v111 = v48[1];
    v49 = *(_QWORD *)qword_143A35358;
    v50 = *(_DWORD *)(*(_QWORD *)(*(_QWORD *)qword_143A35358 + 8LL) + 168LL);
    if ( (v50 & 0x4000000) != 0 )
    {
      v51 = *(_QWORD *)(v49 + 16);
      if ( v51 > 0 )
      {
        v52 = 0;
        while ( 1 )
        {
          v53 = *(_QWORD *)(v49 + 8 * v52 + 24);
          if ( *(int *)(*(_QWORD *)(v53 + 8) + 168LL) >= 0 || (*(_BYTE *)(v53 + 171) & 0x40) == 0 )
            goto LABEL_87;
          if ( v51 == ++v52 )
          {
            v54 = 0;
            while ( (unsigned int)MEMORY[0x13B019020](a1, a2: v111, a3: *(_QWORD *)(v49 + 8 * v54 + 24)) == 0 )
            {
              if ( v51 == ++v54 )
                goto LABEL_62;
            }
            goto LABEL_96;
          }
        }
      }
LABEL_63:
      if ( v48 == (_QWORD *)qword_143A35618 || v48 == nullptr )
      {
        v55 = *(_QWORD *)qword_143A35368;
        v109 = qword_143A35818(a1: &unk_14359FC78);
        v96 = (_QWORD *)a1[39];
        ++*(_QWORD *)v55;
        v48 = (_QWORD *)v109;
        a1[39] = v34;
        v91 = 343;
        if ( v96 == nullptr )
          goto LABEL_146;
        v28 = (*v96)-- == 1;
        if ( !v28 )
          goto LABEL_146;
      }
      else
      {
        v55 = v48[1];
        v56 = v48[5];
        ++*v48;
        v21 = v55;
        ++*(_QWORD *)v55;
        if ( v56 != 0 )
        {
          ++*(_QWORD *)v56;
          if ( v12 == *(_QWORD *)(v56 + 24) )
            *(_DWORD *)(v12 + 40) = *(_DWORD *)(v56 + 36);
          a1[39] = v34;
          v28 = (*v48)-- == 1;
          if ( !v28 )
          {
            if ( v12 != *(_QWORD *)(v56 + 24) )
              goto LABEL_70;
            goto LABEL_130;
          }
          v114 = v56;
          (*(void (__fastcall **)(_QWORD *))(v55 + 48))(a1: v48);
          v56 = v114;
          v107 = 0;
LABEL_172:
          if ( v12 != *(_QWORD *)(v56 + 24) )
          {
            if ( v107 != 0 )
              goto LABEL_163;
LABEL_70:
            v57 = *(_DWORD *)(v12 + 40);
            goto LABEL_114;
          }
LABEL_130:
          v79 = v56;
          goto LABEL_118;
        }
        a1[39] = v34;
        v28 = (*v48)-- == 1;
        if ( !v28 )
          goto LABEL_145;
        v96 = v48;
        v91 = 0;
      }
      (*(void (__fastcall **)(_QWORD *, __int64, __int64))(v96[1] + 48LL))(a1: v96, a2: v56, a3: v21);
      if ( v91 == 0 )
LABEL_145:
        v91 = *(_DWORD *)(v12 + 40);
LABEL_146:
      v79 = *v35;
      if ( *v35 != 0 )
      {
        *v35 = *(_QWORD *)v79;
        *(_QWORD *)v79 = 1;
        --*(_DWORD *)qword_1435FA6D0;
      }
      else
      {
        v79 = MEMORY[0x13B00DD60](a1: qword_143A35A88);
      }
      *(_QWORD *)(v79 + 16) = 0;
      *(_QWORD *)(v79 + 24) = v12;
      ++*(_QWORD *)v12;
      v97 = *(_QWORD *)(v38 + 504);
      *(_DWORD *)(v79 + 32) = -1;
      v98 = *(_QWORD *)(v97 + 16);
      *(_DWORD *)(v79 + 36) = v91;
      v99 = *(_QWORD *)(v98 + 744);
      v100 = *(_QWORD *)(v99 + 8);
      *(_QWORD *)&v101 = v99;
      v102 = v100 | *(_QWORD *)(v79 - 8) & 3LL;
      *(_QWORD *)v100 = v79 - 16;
      *((_QWORD *)&v101 + 1) = v102;
      *(_OWORD *)(v79 - 16) = v101;
      *(_QWORD *)(v99 + 8) = v79 - 16;
      goto LABEL_118;
    }
    if ( v50 >= 0 || (*(_BYTE *)(v49 + 171) & 0x40) == 0 )
    {
LABEL_87:
      v66 = *(_QWORD **)qword_143A35450;
      v67 = qword_143A35818(a1: &unk_14359FD58);
      v68 = (_QWORD *)a1[12];
      v69 = (_QWORD *)a1[13];
      v70 = (_QWORD *)a1[14];
      a1[12] = v66;
      ++*v66;
      a1[13] = v67;
      a1[14] = 0;
      if ( v68 != nullptr )
      {
        v28 = (*v68)-- == 1;
        if ( v28 )
          (*(void (**)(void))(v68[1] + 48LL))();
      }
      if ( v69 != nullptr )
      {
        v28 = (*v69)-- == 1;
        if ( v28 )
          (*(void (__fastcall **)(_QWORD *))(v69[1] + 48LL))(a1: v69);
      }
      if ( v70 != nullptr )
      {
        v28 = (*v70)-- == 1;
        if ( v28 )
          (*(void (__fastcall **)(_QWORD *))(v70[1] + 48LL))(a1: v70);
      }
      goto LABEL_96;
    }
    v74 = *(_QWORD *)(v111 + 8);
    v75 = *(_DWORD *)(v74 + 168);
    if ( (v75 & 0x40000000) != 0 )
    {
      if ( *(int *)(*(_QWORD *)(v74 + 8) + 168LL) < 0 )
        goto LABEL_105;
      v111 = *(_QWORD *)(v111 + 8);
    }
    else if ( v75 < 0 && (*(_BYTE *)(v111 + 171) & 0x40) != 0 )
    {
      v74 = v48[1];
LABEL_105:
      v76 = *(_QWORD *)(v74 + 344);
      if ( v76 == 0 )
      {
        while ( v49 != v74 )
        {
          v74 = *(_QWORD *)(v74 + 256);
          if ( v74 == 0 )
          {
            if ( v49 != qword_143A35760 )
            {
LABEL_62:
              v48 = (_QWORD *)a1[39];
              goto LABEL_63;
            }
            goto LABEL_96;
          }
        }
        goto LABEL_96;
      }
      v77 = *(_QWORD *)(v76 + 16);
      if ( v77 > 0 )
      {
        v78 = 0;
        while ( v49 != *(_QWORD *)(v76 + 8 * v78 + 24) )
        {
          if ( v77 == ++v78 )
            goto LABEL_62;
        }
        goto LABEL_96;
      }
      goto LABEL_63;
    }
    if ( v49 == v111 )
    {
LABEL_96:
      v71 = ((__int64 (*)(void))unk_143218970)();
      if ( v71 != 0 )
      {
        v72 = ((__int64 (__fastcall *)(__int64, __int64))unk_1430EC890)(a1: v71, a2: qword_14393F9B0);
        v73 = (_QWORD *)a1[39];
        v31 = v72;
        if ( v72 != 0 )
        {
          a1[39] = v34;
          if ( v73 != nullptr )
          {
            v28 = (*v73)-- == 1;
            if ( v28 )
              (*(void (**)(void))(v73[1] + 48LL))();
          }
          goto LABEL_73;
        }
        v55 = a1[12];
        v48 = (_QWORD *)a1[13];
        a1[39] = v34;
        v56 = a1[14];
        *((_OWORD *)a1 + 6) = 0;
        a1[14] = 0;
        if ( v73 == nullptr )
        {
          v79 = v56;
          if ( v56 != 0 )
          {
LABEL_162:
            if ( *(_QWORD *)(v56 + 24) != v12 )
            {
LABEL_163:
              v57 = 346;
LABEL_114:
              v79 = *v35;
              if ( *v35 != 0 )
              {
                *v35 = *(_QWORD *)v79;
                *(_QWORD *)v79 = 1;
                --*(_DWORD *)qword_1435FA6D0;
              }
              else
              {
                v112 = v56;
                v106 = MEMORY[0x13B00DD60](a1: qword_143A35A88, a2: v56, a3: v21);
                v56 = v112;
                v79 = v106;
              }
              *(_QWORD *)(v79 + 24) = v12;
              ++*(_QWORD *)v12;
              v80 = *(_QWORD *)(v38 + 504);
              *(_DWORD *)(v79 + 32) = -1;
              v81 = *(_QWORD *)(v80 + 16);
              *(_DWORD *)(v79 + 36) = v57;
              v82 = *(_QWORD *)(v81 + 744);
              v83 = *(_QWORD *)(v82 + 8);
              *(_QWORD *)&v84 = v82;
              v85 = v83 | *(_QWORD *)(v79 - 8) & 3LL;
              *(_QWORD *)v83 = v79 - 16;
              *((_QWORD *)&v84 + 1) = v85;
              *(_OWORD *)(v79 - 16) = v84;
              v28 = *(_QWORD *)v56 == 0;
              *(_QWORD *)(v82 + 8) = v79 - 16;
              *(_QWORD *)(v79 + 16) = v56;
              if ( v28 )
                (*(void (__fastcall **)(__int64))(*(_QWORD *)(v56 + 8) + 48LL))(a1: v56);
            }
LABEL_118:
            ((void (__fastcall *)(__int64, _QWORD))unk_142F544C0)(a1: v12, a2: 0);
            if ( qword_143943D28 == v12 )
            {
              v28 = (*(_QWORD *)v12)-- == 1;
              if ( v28 )
                (*(void (__fastcall **)(__int64))(*(_QWORD *)(v12 + 8) + 48LL))(a1: v12);
              qword_143943D28 = 0;
            }
            v86 = a1[7];
            v87 = *(_QWORD *)(v86 + 8);
            v88 = *(_QWORD *)(v87 + 40);
            v89 = *(_QWORD **)(v88 + 16);
            *(_QWORD *)(v86 + 8) = *(_QWORD *)(v87 + 48);
            *(_DWORD *)(v88 + 64) = -1;
            if ( v89 != nullptr )
            {
              *(_QWORD *)(v88 + 16) = 0;
              v28 = (*v89)-- == 1;
              if ( v28 )
                (*(void (**)(void))(v89[1] + 48LL))();
            }
            v28 = (*(_QWORD *)v88)-- == 1;
            if ( v28 )
              (*(void (__fastcall **)(__int64))(*(_QWORD *)(v88 + 8) + 48LL))(a1: v88);
            v90 = v79;
            *(_QWORD *)(v88 + 120) = 0;
            v31 = 0;
            MEMORY[0x13B00DF80](a1, a2: v55, a3: v48, a4: v90);
            return v31;
          }
          goto LABEL_184;
        }
      }
      else
      {
        ((void (__fastcall *)(_QWORD *, __int64 *, __int64))unk_142F6E530)(a1, a2: &a10, a3: qword_14393F9A8);
        v55 = a10;
        v48 = a11;
        v73 = (_QWORD *)a1[39];
        v56 = (__int64)a12;
        a1[39] = v34;
        if ( v73 == nullptr )
        {
LABEL_160:
          if ( v56 != 0 )
          {
            v79 = v56;
            goto LABEL_162;
          }
          goto LABEL_184;
        }
      }
      v28 = (*v73)-- == 1;
      if ( !v28 )
        goto LABEL_160;
      v113 = v56;
      (*(void (**)(void))(v73[1] + 48LL))();
      v56 = v113;
      if ( v113 == 0 )
      {
LABEL_184:
        v91 = 346;
        goto LABEL_146;
      }
      v107 = 346;
      goto LABEL_172;
    }
    goto LABEL_63;
  }
  v58 = ((__int64 (*)(void))unk_143218970)();
  if ( v58 == 0 )
  {
    ((void (__fastcall *)(_QWORD *, __int64 *, __int64))unk_142F6E530)(a1, a2: &a10, a3: qword_14393F9A8);
    v56 = (__int64)a12;
    v55 = a10;
    v48 = a11;
    if ( a12 != nullptr )
    {
      if ( v12 == a12[3] )
        goto LABEL_130;
LABEL_141:
      v35 = (__int64 *)qword_1435FA6C0;
      v38 = qword_143A35A28;
      v57 = 348;
      goto LABEL_114;
    }
LABEL_153:
    v35 = (__int64 *)qword_1435FA6C0;
    v38 = qword_143A35A28;
    v91 = 348;
    goto LABEL_146;
  }
  v31 = ((__int64 (__fastcall *)(__int64, __int64))unk_1430EC890)(a1: v58, a2: qword_14393F9B0);
  if ( v31 == 0 )
  {
    v56 = a1[14];
    v55 = a1[12];
    a1[14] = 0;
    v48 = (_QWORD *)a1[13];
    *((_OWORD *)a1 + 6) = 0;
    if ( v56 != 0 )
    {
      if ( *(_QWORD *)(v56 + 24) == v12 )
        goto LABEL_130;
      goto LABEL_141;
    }
    goto LABEL_153;
  }
LABEL_73:
  v59 = a1[7];
  v60 = *(_QWORD *)(v59 + 8);
  v61 = *(_QWORD *)(v60 + 40);
  v62 = *(_QWORD **)(v61 + 16);
  *(_QWORD *)(v59 + 8) = *(_QWORD *)(v60 + 48);
  *(_DWORD *)(v61 + 64) = -1;
  if ( v62 != nullptr )
  {
    *(_QWORD *)(v61 + 16) = 0;
    v28 = (*v62)-- == 1;
    if ( v28 )
      (*(void (**)(void))(v62[1] + 48LL))();
  }
  v28 = (*(_QWORD *)v61)-- == 1;
  if ( v28 )
    (*(void (__fastcall **)(__int64))(*(_QWORD *)(v61 + 8) + 48LL))(a1: v61);
  *(_QWORD *)(v61 + 120) = 0;
  return v31;
}