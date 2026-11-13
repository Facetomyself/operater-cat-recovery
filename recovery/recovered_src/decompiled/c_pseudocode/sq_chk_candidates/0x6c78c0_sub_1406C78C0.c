// local variable allocation has failed, the output may be wrong!
// write access to const memory has been detected, the output may be wrong!
__int64 __fastcall sub_1406C78C0(
        _QWORD *a1,
        __int64 a2,
        _QWORD **a3,
        __int64 a4,
        __int64 a5,
        __int64 a6,
        __int64 a7,
        _QWORD *a8,
        __int64 a9,
        __int64 a10,
        __int64 a11,
        __int64 a12)
{
  __int128 v12; // xmm6
  __int64 v13; // rsi
  _QWORD *v14; // r12
  __int64 v16; // rax
  __int64 v17; // rdx
  __int64 v18; // rax
  __int64 v19; // rdx
  _QWORD *v20; // rax
  __int64 v21; // rax
  __int64 v22; // rbx
  __int64 v23; // rax
  __int64 v24; // rax
  bool v25; // zf
  _QWORD *v26; // r15
  __int64 v27; // rax
  __int64 v28; // rax
  _QWORD *v29; // rbp
  __int64 v30; // rax
  _QWORD *v31; // r13
  __int64 v32; // rax
  __int64 v33; // r13
  int v34; // eax
  __int64 v35; // rax
  __int64 v36; // r14
  int v37; // eax
  int v38; // r13d
  __int64 v39; // rdx
  int v40; // eax
  int v41; // r13d
  __int64 v42; // rdx
  int v43; // eax
  int v44; // r13d
  __int64 v45; // rdx
  int v46; // eax
  int v47; // r13d
  _QWORD *v48; // r15
  __int64 v49; // r13
  int v50; // eax
  __int64 v51; // rax
  __int64 v52; // r14
  int v53; // eax
  int v54; // r13d
  __int64 result; // rax
  __int64 v56; // rdx
  __int64 v57; // rcx
  __int64 v58; // rbx
  _QWORD *v59; // rcx
  __int64 v60; // rbp
  _QWORD *v61; // r13
  __int64 v62; // r14
  int v63; // edx
  __int64 v64; // rax
  __int64 v65; // rax
  __int64 v66; // rdx
  unsigned __int64 v67; // r8
  __int128 v68; // xmm0
  __int64 v69; // rax
  __int64 v70; // rax
  __int64 v71; // r15
  __int64 v72; // rax
  __int64 v73; // rdx
  unsigned __int64 v74; // r8
  __int128 v75; // xmm0
  __int64 v76; // rax
  __int64 v77; // rax
  __int64 v78; // rdx
  __int64 v79; // rsi
  _QWORD *v80; // rcx
  __int64 *v81; // rax
  __int64 v82; // rdx
  _QWORD *v83; // rax
  __int64 v84; // rax
  __int64 v85; // rcx
  __int64 v86; // rax
  __int64 v87; // rdx
  __int64 v88; // rbp
  __int64 v89; // rax
  _QWORD *v90; // r13
  __int64 v91; // r14
  __int64 (__fastcall **v92)(__int64, __int64); // rax
  __int64 (__fastcall *v93)(__int64, __int64); // r8
  __int64 v94; // rdx
  __int64 (__fastcall **v95)(__int64, __int64); // rax
  __int64 (__fastcall *v96)(__int64, __int64); // r9
  __int64 (__fastcall **v97)(__int64, __int64); // rax
  __int64 (__fastcall *v98)(__int64, __int64); // r8
  __int64 v99; // rdx
  __int64 v100; // rcx
  __int64 v101; // rax
  _QWORD *v102; // r15
  __int64 v103; // rdx
  __int64 v104; // rax
  __int64 (__fastcall *v105)(__int64, __int64); // r8
  __int64 v106; // rdx
  _QWORD *v107; // r13
  __int64 (__fastcall **v108)(__int64, __int64); // rax
  __int64 (__fastcall *v109)(__int64, __int64); // r8
  __int64 v110; // rax
  __int64 v111; // r9
  __int64 v112; // r8
  __int64 v113; // rdx
  __int64 v114; // r10
  __int64 v115; // rcx
  __int64 v116; // rax
  __int64 v117; // rdx
  __int64 v118; // rdx
  __int64 v119; // rax
  _QWORD *v120; // r13
  __int64 v121; // rax
  __int64 v122; // rax
  __int64 v123; // rax
  _QWORD *v124; // r10
  _QWORD *v125; // r13
  __int64 v126; // rax
  _QWORD *v127; // r10
  _QWORD *v128; // r13
  __int64 (__fastcall **v129)(__int64, __int64); // rax
  __int64 (__fastcall *v130)(__int64, __int64); // r8
  __int64 v131; // rax
  __int64 (__fastcall **v132)(__int64, __int64); // rax
  __int64 (__fastcall *v133)(__int64, __int64); // r9
  __int64 (__fastcall **v134)(__int64, __int64); // rax
  __int64 (__fastcall *v135)(__int64, __int64); // r8
  _QWORD *v136; // r15
  __int64 v137; // rdx
  __int64 v138; // rcx
  __int64 v139; // rax
  __int64 v140; // rdx
  __int64 v141; // rdx
  __int64 (__fastcall *v142)(__int64, __int64); // rax
  __int64 (__fastcall **v143)(__int64, __int64); // rax
  __int64 v144; // rdx
  __int64 v145; // rax
  _QWORD *v146; // r13
  __int64 v147; // rax
  _QWORD *v148; // r15
  __int64 v149; // rax
  _QWORD *v150; // r13
  __int64 v151; // rax
  __int64 v152; // r14
  __int64 v153; // rbp
  _QWORD *v154; // r13
  __int64 (__fastcall **v155)(__int64, __int64); // rax
  __int64 (__fastcall *v156)(__int64, __int64); // r8
  char v157; // al
  char v158; // r13
  __int64 (__fastcall **v159)(__int64, __int64); // rax
  char v160; // r13
  __int64 *v161; // rax
  __int64 v162; // rdx
  _QWORD *v163; // rax
  __int64 (__fastcall *v164)(__int64, __int64); // rax
  __int64 (__fastcall *v165)(__int64, __int64); // r9
  __int64 (__fastcall **v166)(__int64, __int64); // rax
  __int64 (__fastcall *v167)(__int64, __int64); // r8
  _QWORD *v168; // r15
  __int64 v169; // rdx
  __int64 v170; // rcx
  __int64 v171; // rax
  __int64 v172; // rdx
  __int64 v173; // rdx
  __int64 (__fastcall *v174)(__int64, __int64); // rax
  __int64 (__fastcall **v175)(__int64, __int64); // rax
  __int64 v176; // rdx
  __int64 v177; // rbp
  __int64 v178; // rax
  _QWORD *v179; // r14
  _QWORD *v180; // r13
  __int64 (__fastcall **v181)(__int64, __int64); // rax
  __int64 (__fastcall *v182)(__int64, __int64); // r8
  __int64 v183; // rax
  _QWORD *v184; // rax
  __int64 (__fastcall *v185)(__int64, __int64); // r9
  __int64 (__fastcall **v186)(__int64, __int64); // rax
  __int64 (__fastcall *v187)(__int64, __int64); // r8
  _QWORD *v188; // r15
  char v189; // al
  __int64 (__fastcall *v190)(__int64, __int64); // r8
  __int64 v191; // rdx
  __int64 v192; // rdx
  __int64 (__fastcall **v193)(__int64, __int64); // rax
  char v194; // r13
  double v195; // xmm6_8
  __int64 (__fastcall **v196)(__int64, __int64); // rax
  bool v197; // dl
  int v198; // edx
  int v199; // ecx
  __int64 v200; // rdx
  __int64 (__fastcall *v201)(__int64, __int64); // r8
  __int64 (__fastcall **v202)(__int64, __int64); // rax
  __int64 (__fastcall *v203)(__int64, __int64); // r9
  char v204; // al
  __int64 (__fastcall *v205)(__int64, __int64); // r9
  _QWORD *v206; // r15
  __int64 v207; // rdx
  __int64 v208; // r8
  __int64 v209; // rdx
  __int64 (__fastcall *v210)(__int64, __int64); // rax
  _QWORD *v211; // rax
  __int64 (__fastcall **v212)(__int64, __int64); // rax
  __int64 v213; // rax
  char v214; // bp
  __int64 (__fastcall **v215)(__int64, __int64); // rax
  char v216; // r13
  __int64 v217; // rax
  __int64 v218; // rdx
  double v219; // xmm0_8
  double v220; // xmm6_8
  double v221; // xmm6_8
  _QWORD *v222; // rax
  double v223; // xmm6_8
  __int64 v224; // r13
  __int64 v225; // rdx
  __int64 v226; // [rsp+D8h] [rbp+20h]
  __int64 v227; // [rsp+D8h] [rbp+20h]
  __int64 v228; // [rsp+D8h] [rbp+20h]
  __int64 v229; // [rsp+D8h] [rbp+20h]
  int v230; // [rsp+D8h] [rbp+20h]
  int v231; // [rsp+D8h] [rbp+20h]
  __int64 v232; // [rsp+D8h] [rbp+20h]
  __int64 v233; // [rsp+D8h] [rbp+20h]
  __int64 (__fastcall *v234)(__int64, __int64); // [rsp+D8h] [rbp+20h]
  __int64 (__fastcall *v235)(__int64, __int64); // [rsp+D8h] [rbp+20h]
  int v236; // [rsp+D8h] [rbp+20h]
  _QWORD *v237; // [rsp+D8h] [rbp+20h]
  __int64 (__fastcall *v238)(__int64, __int64); // [rsp+D8h] [rbp+20h]
  __int64 (__fastcall *v239)(__int64, __int64); // [rsp+D8h] [rbp+20h]
  __int64 v240; // [rsp+D8h] [rbp+20h]
  __int64 v241; // [rsp+D8h] [rbp+20h]
  int v242; // [rsp+D8h] [rbp+20h]
  __int64 (__fastcall *v243)(__int64, __int64); // [rsp+D8h] [rbp+20h]
  __int64 (__fastcall *v244)(__int64, __int64); // [rsp+D8h] [rbp+20h]
  __int64 v245; // [rsp+D8h] [rbp+20h]
  __int64 v246; // [rsp+D8h] [rbp+20h]
  __int64 (__fastcall *v247)(__int64, __int64); // [rsp+D8h] [rbp+20h]
  __int64 (__fastcall *v248)(__int64, __int64); // [rsp+D8h] [rbp+20h]
  __int64 (__fastcall *v249)(__int64, __int64); // [rsp+D8h] [rbp+20h]
  __int64 (__fastcall *v250)(__int64, __int64); // [rsp+D8h] [rbp+20h]
  __int64 v251; // [rsp+D8h] [rbp+20h]
  __int64 (__fastcall *v252)(__int64, __int64); // [rsp+E0h] [rbp+28h]
  __int64 (__fastcall *v253)(__int64, __int64); // [rsp+E0h] [rbp+28h]

  *(_OWORD *)&a12 = v12;
  v13 = qword_143943E38;
  v14 = *a3;
  if ( qword_143943E38 == 0 )
    goto LABEL_4;
  v16 = *(_QWORD *)qword_143943E38;
  if ( *(__int64 *)qword_143943E38 > 1 )
  {
    *(_QWORD *)qword_143943E38 = v16 - 1;
LABEL_4:
    qword_143943E38 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64, __int64))unk_142F58E90)(
                        a1,
                        a2: qword_143943F60,
                        a3: qword_143943E90,
                        a4: 16);
    v13 = qword_143943E38;
    goto LABEL_5;
  }
  if ( *(_QWORD *)(qword_143943E38 + 16) != 0 )
  {
    v70 = v16 - 1;
    *(_QWORD *)qword_143943E38 = v70;
    if ( v70 == 0 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(qword_143943E38 + 8) + 48LL))(a1: qword_143943E38);
    goto LABEL_4;
  }
LABEL_5:
  v17 = a1[7];
  v18 = *(_QWORD *)(v17 + 8);
  *(_QWORD *)(v13 + 120) = v18;
  *(_QWORD *)(v17 + 8) = v13 + 72;
  if ( v18 != 0
    && (*(_BYTE *)(v18 + 69) == 1
     || *(_QWORD *)(v18 + 56) >= (unsigned __int64)(*(_QWORD *)(v18 + 32)
                                                  + 2LL * *(int *)(*(_QWORD *)(v18 + 32) + 168LL)
                                                  + 184)) )
  {
    v19 = *(_QWORD *)(v13 + 112);
    if ( v19 != 0 )
    {
      v20 = *(_QWORD **)(v18 + 40);
      *(_QWORD *)(v19 + 16) = v20;
      if ( v20 != nullptr )
        ++*v20;
    }
  }
  ++*(_QWORD *)v13;
  *(_DWORD *)(v13 + 64) = 0;
  v21 = ((__int64 (*)(void))unk_143219930)();
  v22 = v21;
  if ( v21 == 0 )
  {
    ((void (__fastcall *)(_QWORD *, _QWORD **, __int64))unk_142F6E530)(a1, a2: &a8, a3: qword_14393F718);
    v61 = a8;
    v62 = a9;
    v63 = 106;
    v60 = a10;
    goto LABEL_91;
  }
  *(_DWORD *)(v13 + 40) = 106;
  v23 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64))unk_142F78640)(a1, a2: v21, a3: qword_14393F720);
  v22 = v23;
  if ( v23 == 0 )
  {
LABEL_114:
    v61 = (_QWORD *)a1[12];
    v62 = a1[13];
    v63 = 106;
    v60 = a1[14];
    *((_OWORD *)a1 + 6) = 0;
    a1[14] = 0;
    goto LABEL_91;
  }
  v24 = ((__int64 (__fastcall *)(__int64, __int64))unk_1430EC890)(a1: v23, a2: qword_14393F728);
  v25 = (*(_QWORD *)v22)-- == 1;
  v26 = (_QWORD *)v24;
  if ( !v25 )
  {
    if ( v24 != 0 )
      goto LABEL_15;
LABEL_80:
    v60 = a1[14];
    v61 = (_QWORD *)a1[12];
    v22 = 0;
    v62 = a1[13];
    v63 = 106;
    *((_OWORD *)a1 + 6) = 0;
    a1[14] = 0;
    if ( v60 != 0 )
      goto LABEL_92;
    goto LABEL_81;
  }
  (*(void (__fastcall **)(__int64))(*(_QWORD *)(v22 + 8) + 48LL))(a1: v22);
  if ( v26 == nullptr )
    goto LABEL_80;
LABEL_15:
  v27 = ((__int64 (*)(void))unk_143219FA0)();
  v22 = v27;
  if ( v27 == 0 )
  {
    ((void (__fastcall *)(_QWORD *, _QWORD **, __int64))unk_142F6E530)(a1, a2: &a8, a3: qword_14393F638);
    v61 = a8;
    v62 = a9;
    v60 = a10;
LABEL_89:
    v25 = (*v26)-- == 1;
    v63 = 106;
    if ( !v25 )
      goto LABEL_91;
    goto LABEL_90;
  }
  v22 = ((__int64 (__fastcall *)(__int64, __int64))unk_1430EC890)(a1: v27, a2: qword_14393F730);
  if ( v22 == 0 )
  {
    v60 = a1[14];
    a1[14] = 0;
    v61 = (_QWORD *)a1[12];
    v62 = a1[13];
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_89;
  }
  v28 = ((__int64 (__fastcall *)(_QWORD *, __int64))unk_1430EC890)(a1: v14, a2: qword_14393F650);
  v29 = (_QWORD *)v28;
  if ( v28 == 0 )
  {
    v61 = (_QWORD *)a1[12];
    v62 = a1[13];
    v60 = a1[14];
    *((_OWORD *)a1 + 6) = 0;
    a1[14] = 0;
    v25 = (*v26)-- == 1;
    if ( v25 )
      (*(void (__fastcall **)(_QWORD *))(v26[1] + 48LL))(a1: v26);
    v25 = (*(_QWORD *)v22)-- == 1;
    if ( v25 )
    {
      v84 = *(_QWORD *)(v22 + 8);
      v85 = v22;
      v22 = 0;
      (*(void (__fastcall **)(__int64))(v84 + 48))(a1: v85);
      v63 = 106;
      goto LABEL_91;
    }
    goto LABEL_128;
  }
  *(_DWORD *)(v13 + 40) = 106;
  v30 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64))unk_142F6A9F0)(a1, a2: v22, a3: v28);
  v25 = (*(_QWORD *)v22)-- == 1;
  v31 = (_QWORD *)v30;
  if ( v25 )
    (*(void (__fastcall **)(__int64))(*(_QWORD *)(v22 + 8) + 48LL))(a1: v22);
  v25 = (*v29)-- == 1;
  if ( v25 )
    (*(void (__fastcall **)(_QWORD *))(v29[1] + 48LL))(a1: v29);
  if ( v31 == nullptr )
  {
    v61 = (_QWORD *)a1[12];
    v62 = a1[13];
    v60 = a1[14];
    *((_OWORD *)a1 + 6) = 0;
    a1[14] = 0;
    v25 = (*v26)-- == 1;
    if ( v25 )
    {
      v22 = 0;
      (*(void (__fastcall **)(_QWORD *))(v26[1] + 48LL))(a1: v26);
      v63 = 106;
      goto LABEL_91;
    }
LABEL_128:
    v22 = 0;
    v63 = 106;
    goto LABEL_91;
  }
  *(_DWORD *)(v13 + 40) = 106;
  a8 = v31;
  v32 = ((__int64 (__fastcall *)(_QWORD *, _QWORD *, _QWORD **, __int64))unk_1430D4C80)(
          a1,
          a2: v26,
          a3: &a8,
          a4: qword_14393F738);
  v25 = (*v26)-- == 1;
  v22 = v32;
  if ( v25 )
    (*(void (__fastcall **)(_QWORD *))(v26[1] + 48LL))(a1: v26);
  v25 = (*v31)-- == 1;
  if ( v25 )
    (*(void (__fastcall **)(_QWORD *))(v31[1] + 48LL))(a1: v31);
  if ( v22 == 0 )
    goto LABEL_114;
  v26 = (_QWORD *)((__int64 (__fastcall *)(_QWORD *, __int64))unk_1430EC890)(a1: v14, a2: qword_14393F658);
  if ( v26 == nullptr )
  {
LABEL_144:
    v61 = (_QWORD *)a1[12];
    v62 = a1[13];
    v63 = 107;
    v60 = a1[14];
    *((_OWORD *)a1 + 6) = 0;
    a1[14] = 0;
    goto LABEL_91;
  }
  v33 = *(_QWORD *)(qword_14393F5F8 + 32);
  if ( *(_BYTE *)(v33 + 10) != 0 )
  {
    v34 = *(_DWORD *)(v33 + 12);
    if ( v34 == 0 )
    {
      v34 = dword_143547A28;
      *(_DWORD *)(v33 + 12) = dword_143547A28++;
    }
    if ( dword_143547A18 == v34 )
    {
      v35 = qword_143943E28;
    }
    else
    {
      dword_143547A18 = v34;
      v35 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
              a1: v33,
              a2: qword_14393F740,
              a3: *(_QWORD *)(qword_14393F740 + 24));
      qword_143943E28 = v35;
    }
    if ( v35 >= 0 )
    {
      v36 = v33 + (1LL << *(_BYTE *)(v33 + 9)) + 32;
      if ( *(_QWORD *)(v36 + 16 * v35 + 8) != 0 )
        goto LABEL_36;
      v131 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
               a1: v33,
               a2: qword_14393F740,
               a3: *(_QWORD *)(qword_14393F740 + 24));
      qword_143943E28 = v131;
      if ( v131 >= 0 )
      {
        v82 = *(_QWORD *)(v36 + 16 * v131 + 8);
LABEL_117:
        if ( v82 != 0 )
          goto LABEL_36;
      }
    }
  }
  else
  {
    v81 = (__int64 *)MEMORY[0x13B02A410](a1: qword_14393F5F8, a2: qword_14393F740);
    if ( v81 != nullptr )
    {
      v82 = *v81;
      goto LABEL_117;
    }
  }
  v83 = (_QWORD *)MEMORY[0x13B02A410](a1: *(_QWORD *)qword_1435FA560, a2: qword_14393F740);
  if ( v83 == nullptr || *v83 == 0 )
  {
    ((void (__fastcall *)(_QWORD *, _QWORD **, __int64))unk_142F6E530)(a1, a2: &a8, a3: qword_14393F740);
    v61 = a8;
    v62 = a9;
    v63 = 107;
    v60 = a10;
    v25 = (*v26)-- == 1;
    if ( !v25 )
      goto LABEL_91;
    goto LABEL_90;
  }
LABEL_36:
  v37 = ((__int64 (__fastcall *)(_QWORD *))unk_1432AA300)(a1: v26);
  v25 = (*v26)-- == 1;
  v38 = v37;
  if ( v25 )
    (*(void (__fastcall **)(_QWORD *))(v26[1] + 48LL))(a1: v26);
  if ( v38 == -1 )
    goto LABEL_144;
  if ( v38 == 1 )
  {
    a7 = v22;
    v87 = ((__int64 (*)(void))unk_143219930)();
    if ( v87 == 0 )
    {
      ((void (__fastcall *)(_QWORD *, _QWORD **, __int64))unk_142F6E530)(a1, a2: &a8, a3: qword_14393F718);
      v61 = a8;
      v62 = a9;
      v60 = a10;
      goto LABEL_206;
    }
    *(_DWORD *)(v13 + 40) = 108;
    v88 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64))unk_142F78640)(a1, a2: v87, a3: qword_14393F748);
    if ( v88 == 0 )
      goto LABEL_205;
    v89 = *(_QWORD *)v22;
    v90 = *(_QWORD **)(v22 + 8);
    v91 = *(_QWORD *)(v88 + 8);
    if ( *(_QWORD *)v22 == 1 )
    {
      v94 = qword_143A35788;
      if ( v90 == (_QWORD *)qword_143A35788 )
      {
        if ( (*(_BYTE *)(v22 + 32) & 3) == 0 )
        {
          if ( v91 == qword_143A35788 )
          {
            if ( *(_QWORD *)(v88 + 16) == 0 )
              goto LABEL_547;
            v157 = ((__int64 (__fastcall *)(_QWORD, __int64 *, __int64))unk_142F5A1C0)(
                     a1: *(_QWORD *)(qword_143A35A28 + 504),
                     a2: &a7,
                     a3: v88);
            v25 = (*(_QWORD *)v88)-- == 1;
            v158 = v157;
            if ( v25 )
              (*(void (__fastcall **)(__int64))(*(_QWORD *)(v88 + 8) + 48LL))(a1: v88);
            if ( v158 != 0 )
              goto LABEL_319;
            goto LABEL_205;
          }
          goto LABEL_136;
        }
        if ( (_QWORD *)v91 != v90 )
        {
LABEL_136:
          v92 = (__int64 (__fastcall **)(__int64, __int64))v90[12];
          if ( v92 == nullptr )
          {
LABEL_242:
            if ( v90 == (_QWORD *)v91 )
              goto LABEL_172;
            goto LABEL_243;
          }
          v93 = v92[19];
          if ( v93 == nullptr )
            goto LABEL_210;
LABEL_138:
          result = v93(a1: v22, a2: v88);
          if ( result != qword_143A35620 )
            goto LABEL_139;
          v25 = (*(_QWORD *)result)-- == 1;
          if ( v25 )
            (*(void (__fastcall **)(__int64))(*(_QWORD *)(result + 8) + 48LL))(a1: result);
          v92 = (__int64 (__fastcall **)(__int64, __int64))v90[12];
          if ( v92 != nullptr )
          {
LABEL_210:
            v96 = *v92;
            if ( v90 == (_QWORD *)v91 )
              goto LABEL_211;
LABEL_152:
            v97 = *(__int64 (__fastcall ***)(__int64, __int64))(v91 + 96);
            if ( v97 != nullptr )
            {
              v98 = *v97;
              if ( *v97 == v96 )
              {
LABEL_211:
                if ( v96 == nullptr )
                  goto LABEL_172;
                v98 = nullptr;
                goto LABEL_213;
              }
              if ( v96 == nullptr )
                goto LABEL_168;
              if ( v98 != nullptr )
              {
                v99 = *(_QWORD *)(v91 + 344);
                if ( v99 != 0 )
                {
                  v100 = *(_QWORD *)(v99 + 16);
                  v101 = 0;
                  if ( v100 <= 0 )
                  {
LABEL_213:
                    v102 = (_QWORD *)qword_143A35620;
                    goto LABEL_165;
                  }
                  while ( *(_QWORD **)(v99 + 8 * v101 + 24) != v90 )
                  {
                    if ( v100 == ++v101 )
                      goto LABEL_213;
                  }
                }
                else
                {
                  v184 = (_QWORD *)v91;
                  while ( 1 )
                  {
                    v184 = (_QWORD *)v184[32];
                    if ( v184 == nullptr )
                      break;
                    if ( v184 == v90 )
                      goto LABEL_161;
                  }
                  if ( v90 != (_QWORD *)qword_143A35760 )
                    goto LABEL_213;
                }
LABEL_161:
                v234 = v96;
                result = v98(a1: v22, a2: v88);
                v102 = (_QWORD *)qword_143A35620;
                if ( result != qword_143A35620 )
                  goto LABEL_139;
                v25 = (*(_QWORD *)qword_143A35620)-- == 1;
                v96 = v234;
                if ( v25 )
                {
                  (*(void (__fastcall **)(__int64))(*(_QWORD *)(qword_143A35620 + 8) + 48LL))(a1: qword_143A35620);
                  v96 = v234;
                }
LABEL_164:
                v98 = nullptr;
LABEL_165:
                v235 = v98;
                result = v96(a1: v22, a2: v88);
                if ( (_QWORD *)result != v102 )
                  goto LABEL_139;
                v25 = (*v102)-- == 1;
                v98 = v235;
                if ( v25 )
                {
                  (*(void (__fastcall **)(_QWORD *, __int64, __int64 (__fastcall *)(__int64, __int64)))(v102[1] + 48LL))(
                    a1: v102,
                    a2: v103,
                    a3: v235);
                  v98 = v235;
                }
LABEL_168:
                if ( v98 != nullptr )
                  goto LABEL_169;
                goto LABEL_172;
              }
            }
            else if ( v96 == nullptr )
            {
              goto LABEL_172;
            }
            v102 = (_QWORD *)qword_143A35620;
            goto LABEL_164;
          }
          goto LABEL_242;
        }
      }
      else if ( v90 != (_QWORD *)v91 )
      {
        v95 = (__int64 (__fastcall **)(__int64, __int64))v90[12];
        if ( v95 == nullptr )
        {
LABEL_243:
          v132 = *(__int64 (__fastcall ***)(__int64, __int64))(v91 + 96);
          if ( v132 != nullptr )
          {
            v98 = *v132;
            if ( *v132 != nullptr )
            {
LABEL_169:
              result = v98(a1: v22, a2: v88);
              if ( result == qword_143A35620 )
              {
                v25 = (*(_QWORD *)result)-- == 1;
                if ( v25 )
                  (*(void (__fastcall **)(__int64))(*(_QWORD *)(result + 8) + 48LL))(a1: result);
                goto LABEL_172;
              }
LABEL_139:
              if ( result != 0 )
                goto LABEL_140;
              goto LABEL_203;
            }
          }
LABEL_172:
          v104 = v90[13];
          if ( v104 == 0
            || (v105 = *(__int64 (__fastcall **)(__int64, __int64))(v104 + 64)) == nullptr
            && (v105 = *(__int64 (__fastcall **)(__int64, __int64))(v104 + 8)) == nullptr )
          {
            qword_143A358D8(a1: *(_QWORD *)qword_143A35450, a2: &unk_14359FE68, a3: v90[3]);
            v25 = (*(_QWORD *)v88)-- == 1;
            if ( !v25 )
              goto LABEL_205;
            goto LABEL_204;
          }
          result = v105(a1: v22, a2: v88);
          goto LABEL_139;
        }
        v93 = v95[19];
        if ( v93 == nullptr )
        {
          v96 = *v95;
          goto LABEL_152;
        }
        goto LABEL_138;
      }
      if ( v91 == qword_143A354B8 )
        goto LABEL_333;
    }
    else
    {
      if ( v90 != (_QWORD *)v91 )
        goto LABEL_134;
      if ( v90 == (_QWORD *)qword_143A354B8 )
      {
        v195 = *(double *)(v88 + 16) + *(double *)(v22 + 16);
LABEL_465:
        *(_QWORD *)v22 = v89 - 1;
        result = ((__int64 (__fastcall *)(_QWORD))unk_1430DB3D0)(a1: *(_QWORD *)(*(_QWORD *)(qword_143A35A28 + 504)
                                                                               + 16LL));
        *(double *)(result + 16) = v195;
        goto LABEL_142;
      }
    }
    if ( v91 != qword_143A35560 )
    {
LABEL_134:
      if ( v90 != (_QWORD *)qword_143A35788 || v91 != qword_143A35788 )
        goto LABEL_136;
      result = ((__int64 (__fastcall *)(_QWORD, __int64, __int64))unk_142F52DC0)(
                 a1: *(_QWORD *)(qword_143A35A28 + 504),
                 a2: v22,
                 a3: v88);
      if ( result != 0 )
        goto LABEL_140;
LABEL_203:
      v25 = (*(_QWORD *)v88)-- == 1;
      if ( v25 )
LABEL_204:
        (*(void (__fastcall **)(__int64))(*(_QWORD *)(v88 + 8) + 48LL))(a1: v88);
LABEL_205:
      v60 = a1[14];
      a1[14] = 0;
      v61 = (_QWORD *)a1[12];
      v62 = a1[13];
      *((_OWORD *)a1 + 6) = 0;
LABEL_206:
      v63 = 108;
      goto LABEL_91;
    }
    v111 = *(_QWORD *)(v22 + 16);
    v112 = *(_QWORD *)(v88 + 16);
    if ( v111 < 0 )
    {
      v117 = -v111;
      if ( -v111 > 1 )
      {
        v114 = -v112;
        if ( v112 > 0 )
          v114 = *(_QWORD *)(v88 + 16);
        if ( v89 != 1 )
        {
          v115 = v22 + 24;
          v116 = v88 + 24;
          goto LABEL_513;
        }
        v113 = v88 + 24;
LABEL_600:
        if ( v112 < 0 )
        {
          result = ((__int64 (__fastcall *)(__int64, __int64, __int64))unk_1430DA500)(a1: v22, a2: v113, a3: v114);
          v225 = -*(_QWORD *)(result + 16);
          if ( *(__int64 *)(result + 16) <= 0 )
            v225 = *(_QWORD *)(result + 16);
          *(_QWORD *)(result + 16) = v225;
        }
        else
        {
          result = ((__int64 (__fastcall *)(__int64, __int64, __int64, __int64))unk_1430DAA00)(
                     a1: v22,
                     a2: v113,
                     a3: v114,
                     a4: 0xFFFFFFFFLL);
        }
        goto LABEL_142;
      }
    }
    else if ( v111 > 1 )
    {
      v113 = v88 + 24;
      v114 = -v112;
      if ( v112 > 0 )
        v114 = *(_QWORD *)(v88 + 16);
      if ( v89 != 1 )
      {
        v115 = v22 + 24;
        v116 = v88 + 24;
        v117 = *(_QWORD *)(v22 + 16);
LABEL_201:
        if ( v112 < 0 )
        {
          result = ((__int64 (__fastcall *)(__int64, __int64, __int64, __int64))unk_1430DA780)(
                     a1: v115,
                     a2: v117,
                     a3: v116,
                     a4: v114);
          goto LABEL_140;
        }
        result = ((__int64 (__fastcall *)(__int64, __int64, __int64, __int64))unk_1430DA3E0)(
                   a1: v115,
                   a2: v117,
                   a3: v116,
                   a4: v114);
        if ( result != 0 )
          goto LABEL_140;
        goto LABEL_203;
      }
LABEL_613:
      if ( v112 < 0 )
        result = ((__int64 (__fastcall *)(__int64, __int64, __int64, __int64))unk_1430DAA00)(
                   a1: v22,
                   a2: v113,
                   a3: v114,
                   a4: 1);
      else
        result = ((__int64 (__fastcall *)(__int64, __int64, __int64))unk_1430DA500)(a1: v22, a2: v113, a3: v114);
LABEL_142:
      v25 = (*(_QWORD *)v88)-- == 1;
      if ( v25 )
      {
        v233 = result;
        (*(void (__fastcall **)(__int64))(*(_QWORD *)(v88 + 8) + 48LL))(a1: v88);
        result = v233;
      }
      goto LABEL_70;
    }
    if ( v112 < 0 )
      v197 = -v112 <= 1;
    else
      v197 = v112 <= 1;
    if ( v197 )
    {
      if ( v111 < 0 )
      {
        v198 = -*(_DWORD *)(v22 + 24);
      }
      else
      {
        v198 = 0;
        if ( v111 != 0 )
          v198 = *(_DWORD *)(v22 + 24);
      }
      if ( v112 < 0 )
      {
        v199 = -*(_DWORD *)(v88 + 24);
      }
      else
      {
        v199 = 0;
        if ( v112 != 0 )
          v199 = *(_DWORD *)(v88 + 24);
      }
      v200 = (unsigned int)(v199 + v198);
      if ( v89 == 1 )
      {
        ((void (__fastcall *)(__int64 *, __int64))unk_1430DA1B0)(a1: &a7, a2: v200);
        v25 = (*(_QWORD *)v88)-- == 1;
        if ( v25 )
          (*(void (__fastcall **)(__int64))(*(_QWORD *)(v88 + 8) + 48LL))(a1: v88);
        goto LABEL_319;
      }
      result = ((__int64 (__fastcall *)(_QWORD))unk_1430DA0B0)(a1: (unsigned int)v200);
      goto LABEL_140;
    }
    v114 = -v112;
    if ( v112 > 0 )
      v114 = *(_QWORD *)(v88 + 16);
    if ( v89 != 1 )
    {
      v115 = v22 + 24;
      v217 = -v111;
      if ( v111 > 0 )
        v217 = *(_QWORD *)(v22 + 16);
      v117 = v217;
      v116 = v88 + 24;
      if ( v111 >= 0 )
        goto LABEL_201;
LABEL_513:
      if ( v112 < 0 )
      {
        result = ((__int64 (__fastcall *)(__int64, __int64, __int64, __int64))unk_1430DA3E0)(
                   a1: v115,
                   a2: v117,
                   a3: v116,
                   a4: v114);
        *(_QWORD *)(result + 16) = -*(_QWORD *)(result + 16);
      }
      else
      {
        result = ((__int64 (__fastcall *)(__int64, __int64, __int64, __int64))unk_1430DA780)(
                   a1: v116,
                   a2: v114,
                   a3: v115,
                   a4: v117);
      }
      goto LABEL_140;
    }
    v113 = v88 + 24;
    if ( v111 >= 0 )
      goto LABEL_613;
    goto LABEL_600;
  }
  v26 = (_QWORD *)((__int64 (__fastcall *)(_QWORD *, __int64))unk_1430EC890)(a1: v14, a2: qword_14393F658);
  if ( v26 != nullptr )
  {
    v39 = ((__int64 (*)(void))unk_143219D20)();
    if ( v39 == 0 )
    {
      ((void (__fastcall *)(_QWORD *, _QWORD **, __int64))unk_142F6E530)(a1, a2: &a8, a3: qword_14393F750);
      v61 = a8;
      v62 = a9;
      v63 = 109;
      v60 = a10;
      v25 = (*v26)-- == 1;
      if ( !v25 )
        goto LABEL_91;
      goto LABEL_90;
    }
    v40 = ((__int64 (__fastcall *)(_QWORD *, __int64))unk_1432AA300)(a1: v26, a2: v39);
    v25 = (*v26)-- == 1;
    v41 = v40;
    if ( v25 )
      (*(void (__fastcall **)(_QWORD *))(v26[1] + 48LL))(a1: v26);
    if ( v41 != -1 )
    {
      if ( v41 == 1 )
      {
        a7 = v22;
        v106 = ((__int64 (*)(void))unk_143219930)();
        if ( v106 == 0 )
        {
          ((void (__fastcall *)(_QWORD *, _QWORD **, __int64))unk_142F6E530)(a1, a2: &a8, a3: qword_14393F718);
          v61 = a8;
          v62 = a9;
          v60 = a10;
          goto LABEL_190;
        }
        *(_DWORD *)(v13 + 40) = 110;
        v88 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64))unk_142F78640)(a1, a2: v106, a3: qword_14393F758);
        if ( v88 == 0 )
          goto LABEL_189;
        v89 = *(_QWORD *)v22;
        v91 = *(_QWORD *)(v88 + 8);
        v107 = *(_QWORD **)(v22 + 8);
        if ( *(_QWORD *)v22 != 1 )
        {
          if ( (_QWORD *)v91 != v107 )
          {
LABEL_181:
            if ( v107 == (_QWORD *)qword_143A35788 && v91 == qword_143A35788 )
            {
              result = ((__int64 (__fastcall *)(_QWORD, __int64, __int64))unk_142F52DC0)(
                         a1: *(_QWORD *)(qword_143A35A28 + 504),
                         a2: v22,
                         a3: v88);
              if ( result != 0 )
                goto LABEL_428;
LABEL_187:
              v25 = (*(_QWORD *)v88)-- == 1;
              if ( v25 )
LABEL_188:
                (*(void (__fastcall **)(__int64))(*(_QWORD *)(v88 + 8) + 48LL))(a1: v88);
LABEL_189:
              v60 = a1[14];
              a1[14] = 0;
              v61 = (_QWORD *)a1[12];
              v62 = a1[13];
              *((_OWORD *)a1 + 6) = 0;
LABEL_190:
              v63 = 110;
              goto LABEL_91;
            }
            goto LABEL_183;
          }
          if ( v91 == qword_143A354B8 )
          {
LABEL_534:
            v195 = *(double *)(v22 + 16) + *(double *)(v88 + 16);
            goto LABEL_465;
          }
          goto LABEL_325;
        }
        v94 = qword_143A35788;
        if ( v107 != (_QWORD *)qword_143A35788 )
        {
          if ( (_QWORD *)v91 != v107 )
          {
            v143 = (__int64 (__fastcall **)(__int64, __int64))v107[12];
            if ( v143 == nullptr )
            {
LABEL_321:
              v159 = *(__int64 (__fastcall ***)(__int64, __int64))(v91 + 96);
              if ( v159 != nullptr )
              {
                v135 = *v159;
                if ( *v159 == nullptr )
                  goto LABEL_272;
LABEL_269:
                result = v135(a1: v22, a2: v88);
                if ( result != qword_143A35620 )
                  goto LABEL_186;
                v25 = (*(_QWORD *)result)-- == 1;
                if ( v25 )
                  (*(void (__fastcall **)(__int64))(*(_QWORD *)(result + 8) + 48LL))(a1: result);
              }
LABEL_272:
              v141 = v107[13];
              if ( v141 == 0
                || (v142 = *(__int64 (__fastcall **)(__int64, __int64))(v141 + 64)) == nullptr
                && (v142 = *(__int64 (__fastcall **)(__int64, __int64))(v141 + 8)) == nullptr )
              {
                qword_143A358D8(a1: *(_QWORD *)qword_143A35450, a2: &unk_14359FE68, a3: v107[3]);
                v25 = (*(_QWORD *)v88)-- == 1;
                if ( !v25 )
                  goto LABEL_189;
                goto LABEL_188;
              }
              result = v142(a1: v22, a2: v88);
LABEL_186:
              if ( result == 0 )
                goto LABEL_187;
LABEL_140:
              v25 = (*(_QWORD *)v22)-- == 1;
              if ( v25 )
              {
                v232 = result;
                (*(void (__fastcall **)(__int64))(*(_QWORD *)(v22 + 8) + 48LL))(a1: v22);
                result = v232;
              }
              goto LABEL_142;
            }
            v109 = v143[19];
            if ( v109 == nullptr )
            {
              v133 = *v143;
LABEL_252:
              v134 = *(__int64 (__fastcall ***)(__int64, __int64))(v91 + 96);
              if ( v134 != nullptr )
              {
                v135 = *v134;
                if ( *v134 != v133 )
                {
                  if ( v133 == nullptr )
                    goto LABEL_268;
                  v136 = (_QWORD *)qword_143A35620;
                  if ( v135 != nullptr )
                  {
                    v137 = *(_QWORD *)(v91 + 344);
                    if ( v137 != 0 )
                    {
                      v138 = *(_QWORD *)(v137 + 16);
                      v139 = 0;
                      if ( v138 <= 0 )
                      {
LABEL_277:
                        v136 = (_QWORD *)qword_143A35620;
                        goto LABEL_265;
                      }
                      while ( *(_QWORD **)(v137 + 8 * v139 + 24) != v107 )
                      {
                        if ( v138 == ++v139 )
                          goto LABEL_277;
                      }
                    }
                    else
                    {
                      v211 = (_QWORD *)v91;
                      while ( v211 != v107 )
                      {
                        v211 = (_QWORD *)v211[32];
                        if ( v211 == nullptr )
                        {
                          if ( v107 == (_QWORD *)qword_143A35760 )
                            break;
                          goto LABEL_277;
                        }
                      }
                    }
                    v238 = v133;
                    result = v135(a1: v22, a2: v88);
                    v136 = (_QWORD *)qword_143A35620;
                    if ( result != qword_143A35620 )
                      goto LABEL_186;
                    v25 = (*(_QWORD *)qword_143A35620)-- == 1;
                    v133 = v238;
                    if ( v25 )
                    {
                      MEMORY[0x13B0039F0](a1: qword_143A35620);
                      v133 = v238;
                    }
                  }
                  v135 = nullptr;
LABEL_265:
                  v239 = v135;
                  result = v133(a1: v22, a2: v88);
                  if ( (_QWORD *)result != v136 )
                    goto LABEL_186;
                  v25 = (*v136)-- == 1;
                  v135 = v239;
                  if ( v25 )
                  {
                    (*(void (__fastcall **)(_QWORD *, __int64, __int64 (__fastcall *)(__int64, __int64)))(v136[1] + 48LL))(
                      a1: v136,
                      a2: v140,
                      a3: v239);
                    v135 = v239;
                  }
LABEL_268:
                  if ( v135 == nullptr )
                    goto LABEL_272;
                  goto LABEL_269;
                }
              }
LABEL_275:
              if ( v133 == nullptr )
                goto LABEL_272;
              v135 = nullptr;
              goto LABEL_277;
            }
            goto LABEL_185;
          }
LABEL_394:
          if ( v91 != qword_143A354B8 )
          {
LABEL_325:
            if ( v91 != qword_143A35560 )
              goto LABEL_181;
            v160 = ((__int64 (__fastcall *)(__int64 *, __int64))unk_1430E28C0)(a1: &a7, a2: v88);
LABEL_327:
            v25 = (*(_QWORD *)v88)-- == 1;
            if ( v25 )
              (*(void (__fastcall **)(__int64))(*(_QWORD *)(v88 + 8) + 48LL))(a1: v88);
            if ( v160 != 0 )
              goto LABEL_319;
            goto LABEL_189;
          }
LABEL_333:
          *(double *)(v22 + 16) = *(double *)(v22 + 16) + *(double *)(v88 + 16);
          goto LABEL_334;
        }
        if ( (*(_BYTE *)(v22 + 32) & 3) != 0 )
        {
          if ( (_QWORD *)v91 == v107 )
            goto LABEL_394;
        }
        else if ( v91 == qword_143A35788 )
        {
          if ( *(_QWORD *)(v88 + 16) != 0 )
          {
            v160 = ((__int64 (__fastcall *)(_QWORD, __int64 *, __int64))unk_142F5A1C0)(
                     a1: *(_QWORD *)(qword_143A35A28 + 504),
                     a2: &a7,
                     a3: v88);
            goto LABEL_327;
          }
LABEL_547:
          v25 = (*(_QWORD *)v88)-- == 1;
          if ( v25 )
            (*(void (__fastcall **)(__int64))(v94 + 48))(a1: v88);
          goto LABEL_336;
        }
LABEL_183:
        v108 = (__int64 (__fastcall **)(__int64, __int64))v107[12];
        if ( v108 == nullptr )
        {
LABEL_320:
          if ( (_QWORD *)v91 == v107 )
            goto LABEL_272;
          goto LABEL_321;
        }
        v109 = v108[19];
        if ( v109 == nullptr )
          goto LABEL_251;
LABEL_185:
        result = v109(a1: v22, a2: v88);
        if ( result != qword_143A35620 )
          goto LABEL_186;
        v25 = (*(_QWORD *)result)-- == 1;
        if ( v25 )
          (*(void (__fastcall **)(__int64))(*(_QWORD *)(result + 8) + 48LL))(a1: result);
        v108 = (__int64 (__fastcall **)(__int64, __int64))v107[12];
        if ( v108 != nullptr )
        {
LABEL_251:
          v133 = *v108;
          if ( (_QWORD *)v91 == v107 )
            goto LABEL_275;
          goto LABEL_252;
        }
        goto LABEL_320;
      }
      v26 = (_QWORD *)((__int64 (__fastcall *)(_QWORD *, __int64))unk_1430EC890)(a1: v14, a2: qword_14393F658);
      if ( v26 != nullptr )
      {
        v42 = ((__int64 (*)(void))unk_143219BD0)();
        if ( v42 == 0 )
        {
          ((void (__fastcall *)(_QWORD *, _QWORD **, __int64))unk_142F6E530)(a1, a2: &a8, a3: qword_14393F760);
          v61 = a8;
          v62 = a9;
          v63 = 111;
          v60 = a10;
          v25 = (*v26)-- == 1;
          if ( !v25 )
            goto LABEL_91;
          goto LABEL_90;
        }
        v43 = ((__int64 (__fastcall *)(_QWORD *, __int64))unk_1432AA300)(a1: v26, a2: v42);
        v25 = (*v26)-- == 1;
        v44 = v43;
        if ( v25 )
          (*(void (__fastcall **)(_QWORD *))(v26[1] + 48LL))(a1: v26);
        if ( v44 != -1 )
        {
          if ( v44 != 1 )
          {
            v26 = (_QWORD *)((__int64 (__fastcall *)(_QWORD *, __int64))unk_1430EC890)(a1: v14, a2: qword_14393F658);
            if ( v26 == nullptr )
              goto LABEL_310;
            v45 = ((__int64 (*)(void))unk_143219A80)();
            if ( v45 != 0 )
            {
              v46 = ((__int64 (__fastcall *)(_QWORD *, __int64))unk_1432AA300)(a1: v26, a2: v45);
              v25 = (*v26)-- == 1;
              v47 = v46;
              if ( v25 )
                (*(void (__fastcall **)(_QWORD *))(v26[1] + 48LL))(a1: v26);
              if ( v47 != -1 )
              {
                if ( v47 != 1 )
                {
                  v48 = (_QWORD *)((__int64 (__fastcall *)(_QWORD *, __int64))unk_1430EC890)(
                                    a1: v14,
                                    a2: qword_14393F658);
                  if ( v48 == nullptr )
                    goto LABEL_354;
                  v49 = *(_QWORD *)(qword_14393F5F8 + 32);
                  if ( *(_BYTE *)(v49 + 10) != 0 )
                  {
                    v50 = *(_DWORD *)(v49 + 12);
                    if ( v50 == 0 )
                    {
                      v50 = dword_143547A28;
                      *(_DWORD *)(v49 + 12) = dword_143547A28++;
                    }
                    if ( dword_143547A1C == v50 )
                    {
                      v51 = qword_143943E30;
                    }
                    else
                    {
                      dword_143547A1C = v50;
                      v51 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
                              a1: v49,
                              a2: qword_14393F798,
                              a3: *(_QWORD *)(qword_14393F798 + 24));
                      qword_143943E30 = v51;
                    }
                    if ( v51 >= 0 )
                    {
                      v52 = v49 + (1LL << *(_BYTE *)(v49 + 9)) + 32;
                      if ( *(_QWORD *)(v52 + 16 * v51 + 8) != 0 )
                        goto LABEL_66;
                      v213 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
                               a1: v49,
                               a2: qword_14393F798,
                               a3: *(_QWORD *)(qword_14393F798 + 24));
                      qword_143943E30 = v213;
                      if ( v213 >= 0 )
                      {
                        v162 = *(_QWORD *)(v52 + 16 * v213 + 8);
LABEL_340:
                        if ( v162 != 0 )
                          goto LABEL_66;
                      }
                    }
                  }
                  else
                  {
                    v161 = (__int64 *)MEMORY[0x13B02A410](a1: qword_14393F5F8, a2: qword_14393F798);
                    if ( v161 != nullptr )
                    {
                      v162 = *v161;
                      goto LABEL_340;
                    }
                  }
                  v163 = (_QWORD *)MEMORY[0x13B02A410](a1: *(_QWORD *)qword_1435FA560, a2: qword_14393F798);
                  if ( v163 == nullptr || *v163 == 0 )
                  {
                    ((void (__fastcall *)(_QWORD *, _QWORD **, __int64))unk_142F6E530)(a1, a2: &a8, a3: qword_14393F798);
                    v61 = a8;
                    v62 = a9;
                    v63 = 117;
                    v60 = a10;
                    v25 = (*v48)-- == 1;
                    if ( !v25 )
                      goto LABEL_91;
                    goto LABEL_344;
                  }
LABEL_66:
                  v53 = ((__int64 (__fastcall *)(_QWORD *))unk_1432AA300)(a1: v48);
                  v25 = (*v48)-- == 1;
                  v54 = v53;
                  if ( v25 )
                    (*(void (__fastcall **)(_QWORD *))(v48[1] + 48LL))(a1: v48);
                  if ( v54 != -1 )
                  {
                    result = v22;
                    if ( v54 != 1 )
                      goto LABEL_70;
                    a7 = v22;
                    v176 = ((__int64 (*)(void))unk_143219930)();
                    if ( v176 == 0 )
                    {
                      ((void (__fastcall *)(_QWORD *, _QWORD **, __int64))unk_142F6E530)(
                        a1,
                        a2: &a8,
                        a3: qword_14393F718);
                      v61 = a8;
                      v62 = a9;
                      v60 = a10;
                      goto LABEL_533;
                    }
                    *(_DWORD *)(v13 + 40) = 118;
                    v177 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64))unk_142F78640)(
                             a1,
                             a2: v176,
                             a3: qword_14393F7A0);
                    if ( v177 == 0 )
                      goto LABEL_532;
                    v178 = *(_QWORD *)v22;
                    v179 = *(_QWORD **)(v177 + 8);
                    v180 = *(_QWORD **)(v22 + 8);
                    if ( *(_QWORD *)v22 == 1 )
                    {
                      if ( v180 != (_QWORD *)qword_143A35788 )
                      {
                        if ( v179 != v180 )
                        {
                          v215 = (__int64 (__fastcall **)(__int64, __int64))v180[12];
                          if ( v215 == nullptr )
                          {
LABEL_588:
                            v201 = nullptr;
                            goto LABEL_492;
                          }
                          v182 = v215[19];
                          if ( v182 == nullptr )
                          {
                            v201 = *v215;
LABEL_492:
                            v202 = (__int64 (__fastcall **)(__int64, __int64))v179[12];
                            if ( v202 == nullptr )
                            {
                              if ( v201 != nullptr )
                                goto LABEL_595;
LABEL_505:
                              v209 = v180[13];
                              if ( v209 == 0
                                || (v210 = *(__int64 (__fastcall **)(__int64, __int64))(v209 + 64)) == nullptr
                                && (v210 = *(__int64 (__fastcall **)(__int64, __int64))(v209 + 8)) == nullptr )
                              {
                                qword_143A358D8(a1: *(_QWORD *)qword_143A35450, a2: &unk_14359FE68, a3: v180[3]);
                                v25 = (*(_QWORD *)v177)-- == 1;
                                if ( v25 )
LABEL_531:
                                  MEMORY[0x13B0039F0](a1: v177);
LABEL_532:
                                v60 = a1[14];
                                v61 = (_QWORD *)a1[12];
                                a1[14] = 0;
                                v62 = a1[13];
                                *((_OWORD *)a1 + 6) = 0;
LABEL_533:
                                v63 = 118;
                                goto LABEL_91;
                              }
                              v183 = v210(a1: v22, a2: v177);
LABEL_410:
                              if ( v183 != 0 )
                              {
                                v25 = (*(_QWORD *)v22)-- == 1;
                                if ( v25 )
                                {
                                  v245 = v183;
                                  MEMORY[0x13B0039F0](a1: v22);
                                  v183 = v245;
                                }
                                goto LABEL_413;
                              }
LABEL_616:
                              v25 = (*(_QWORD *)v177)-- == 1;
                              if ( !v25 )
                                goto LABEL_532;
                              goto LABEL_531;
                            }
                            v203 = *v202;
                            if ( *v202 != v201 )
                            {
                              if ( v201 == nullptr )
                                goto LABEL_501;
                              if ( v203 != nullptr )
                              {
                                v253 = *v202;
                                v249 = v201;
                                v204 = ((__int64 (__fastcall *)(_QWORD *, _QWORD *))unk_1430DB000)(a1: v179, a2: v180);
                                v201 = v249;
                                v205 = v253;
                                if ( v204 == 0 )
                                {
                                  v206 = (_QWORD *)qword_143A35620;
LABEL_498:
                                  v250 = v205;
                                  v183 = v201(a1: v22, a2: v177);
                                  if ( (_QWORD *)v183 != v206 )
                                    goto LABEL_410;
                                  v25 = (*v206)-- == 1;
                                  v203 = v250;
                                  if ( v25 )
                                  {
                                    MEMORY[0x13B0039F0](a1: v206, a2: v207, a3: v208, a4: v250);
                                    v203 = v250;
                                  }
LABEL_501:
                                  if ( v203 != nullptr )
                                  {
                                    v183 = v203(a1: v22, a2: v177);
                                    if ( v183 != qword_143A35620 )
                                      goto LABEL_410;
                                    v25 = (*(_QWORD *)v183)-- == 1;
                                    if ( v25 )
                                      MEMORY[0x13B0039F0](a1: v183);
                                  }
                                  goto LABEL_505;
                                }
                                v183 = v253(a1: v22, a2: v177);
                                v206 = (_QWORD *)qword_143A35620;
                                if ( v183 != qword_143A35620 )
                                  goto LABEL_410;
                                v25 = (*(_QWORD *)qword_143A35620)-- == 1;
                                v201 = v249;
                                if ( v25 )
                                {
                                  MEMORY[0x13B0039F0](a1: qword_143A35620, a2: v218, a3: v249);
                                  v201 = v249;
                                }
LABEL_575:
                                v205 = nullptr;
                                goto LABEL_498;
                              }
LABEL_595:
                              v206 = (_QWORD *)qword_143A35620;
                              goto LABEL_575;
                            }
LABEL_574:
                            v206 = (_QWORD *)qword_143A35620;
                            if ( v201 != nullptr )
                              goto LABEL_575;
                            goto LABEL_505;
                          }
                          goto LABEL_409;
                        }
                        if ( v179 != (_QWORD *)qword_143A354B8 )
                          goto LABEL_555;
                        v223 = *(double *)(v177 + 16) + *(double *)(v22 + 16);
                        goto LABEL_620;
                      }
                      if ( (*(_BYTE *)(v22 + 32) & 3) == 0 )
                      {
                        if ( v179 != v180 )
                          goto LABEL_407;
                        if ( *(_QWORD *)(v177 + 16) == 0 )
                          goto LABEL_414;
                        v216 = ((__int64 (__fastcall *)(_QWORD, __int64 *, __int64))unk_142F5A1C0)(
                                 a1: *(_QWORD *)(qword_143A35A28 + 504),
                                 a2: &a7,
                                 a3: v177);
                        goto LABEL_557;
                      }
                    }
                    if ( v179 != v180 )
                      goto LABEL_405;
                    if ( v179 != (_QWORD *)qword_143A354B8 )
                    {
LABEL_555:
                      if ( v179 != (_QWORD *)qword_143A35560 )
                      {
LABEL_405:
                        if ( v179 != (_QWORD *)qword_143A35788 || v180 != (_QWORD *)qword_143A35788 )
                        {
LABEL_407:
                          v181 = (__int64 (__fastcall **)(__int64, __int64))v180[12];
                          if ( v181 == nullptr )
                            goto LABEL_587;
                          v182 = v181[19];
                          if ( v182 == nullptr )
                          {
LABEL_491:
                            v201 = *v181;
                            if ( v179 == v180 )
                              goto LABEL_574;
                            goto LABEL_492;
                          }
LABEL_409:
                          v183 = v182(a1: v22, a2: v177);
                          if ( v183 != qword_143A35620 )
                            goto LABEL_410;
                          v25 = (*(_QWORD *)v183)-- == 1;
                          if ( v25 )
                            MEMORY[0x13B0039F0](a1: v183);
                          v181 = (__int64 (__fastcall **)(__int64, __int64))v180[12];
                          if ( v181 == nullptr )
                          {
LABEL_587:
                            if ( v179 == v180 )
                              goto LABEL_505;
                            goto LABEL_588;
                          }
                          goto LABEL_491;
                        }
                        v224 = ((__int64 (__fastcall *)(_QWORD, __int64, __int64))unk_142F52DC0)(
                                 a1: *(_QWORD *)(qword_143A35A28 + 504),
                                 a2: v22,
                                 a3: v177);
                        if ( v224 == 0 )
                          goto LABEL_616;
                        v25 = (*(_QWORD *)v22)-- == 1;
                        if ( v25 )
                          MEMORY[0x13B0039F0](a1: v22);
                        a7 = v224;
LABEL_414:
                        v25 = (*(_QWORD *)v177)-- == 1;
                        if ( !v25 )
                        {
LABEL_319:
                          result = a7;
                          goto LABEL_70;
                        }
LABEL_415:
                        MEMORY[0x13B0039F0](a1: v177);
                        goto LABEL_319;
                      }
                      v216 = ((__int64 (__fastcall *)(__int64 *, __int64))unk_1430E28C0)(a1: &a7, a2: v177);
LABEL_557:
                      v25 = (*(_QWORD *)v177)-- == 1;
                      if ( v25 )
                        MEMORY[0x13B0039F0](a1: v177);
                      if ( v216 != 0 )
                        goto LABEL_319;
                      goto LABEL_532;
                    }
                    v223 = *(double *)(v22 + 16) + *(double *)(v177 + 16);
                    if ( v178 != 1 )
                    {
                      *(_QWORD *)v22 = v178 - 1;
                      v183 = ((__int64 (__fastcall *)(_QWORD))unk_1430DB3D0)(a1: *(_QWORD *)(*(_QWORD *)(qword_143A35A28 + 504)
                                                                                           + 16LL));
                      *(double *)(v183 + 16) = v223;
LABEL_413:
                      a7 = v183;
                      goto LABEL_414;
                    }
LABEL_620:
                    *(double *)(v22 + 16) = v223;
                    v25 = (*(_QWORD *)v177)-- == 1;
                    if ( !v25 )
                      goto LABEL_319;
                    goto LABEL_415;
                  }
LABEL_354:
                  v61 = (_QWORD *)a1[12];
                  v62 = a1[13];
                  v63 = 117;
                  v60 = a1[14];
                  *((_OWORD *)a1 + 6) = 0;
                  a1[14] = 0;
                  goto LABEL_91;
                }
                a7 = v22;
                v144 = ((__int64 (*)(void))unk_143219930)();
                if ( v144 == 0 )
                {
                  ((void (__fastcall *)(_QWORD *, _QWORD **, __int64))unk_142F6E530)(a1, a2: &a8, a3: qword_14393F718);
                  v61 = a8;
                  v62 = a9;
                  v60 = a10;
                  goto LABEL_353;
                }
                *(_DWORD *)(v13 + 40) = 116;
                v145 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64))unk_142F78640)(
                         a1,
                         a2: v144,
                         a3: qword_14393F788);
                v146 = (_QWORD *)v145;
                if ( v145 == 0 )
                  goto LABEL_352;
                v147 = ((__int64 (__fastcall *)(__int64, __int64))unk_1430EC890)(a1: v145, a2: qword_14393F728);
                v25 = (*v146)-- == 1;
                v148 = (_QWORD *)v147;
                if ( v25 )
                  (*(void (__fastcall **)(_QWORD *))(v146[1] + 48LL))(a1: v146);
                if ( v148 == nullptr )
                  goto LABEL_352;
                v149 = ((__int64 (__fastcall *)(_QWORD *, __int64))unk_1430EC890)(a1: v14, a2: qword_14393F688);
                v150 = (_QWORD *)v149;
                if ( v149 == 0 )
                {
                  v61 = (_QWORD *)a1[12];
                  v62 = a1[13];
                  v60 = a1[14];
                  *((_OWORD *)a1 + 6) = 0;
                  a1[14] = 0;
                  v25 = (*v148)-- == 1;
                  if ( v25 )
                    MEMORY[0x13B0039F0](a1: v148);
                  goto LABEL_353;
                }
                *(_DWORD *)(v13 + 40) = 116;
                a8 = (_QWORD *)v149;
                v151 = ((__int64 (__fastcall *)(_QWORD *, _QWORD *, _QWORD **, __int64))unk_1430D4C80)(
                         a1,
                         a2: v148,
                         a3: &a8,
                         a4: qword_14393F790);
                v25 = (*v148)-- == 1;
                v152 = v151;
                if ( v25 )
                  (*(void (__fastcall **)(_QWORD *))(v148[1] + 48LL))(a1: v148);
                v25 = (*v150)-- == 1;
                if ( v25 )
                  (*(void (__fastcall **)(_QWORD *))(v150[1] + 48LL))(a1: v150);
                if ( v152 == 0 )
                  goto LABEL_352;
                v153 = *(_QWORD *)(v152 + 8);
                v154 = *(_QWORD **)(v22 + 8);
                if ( *(_QWORD *)v22 != 1 )
                {
                  if ( (_QWORD *)v153 != v154 )
                  {
LABEL_300:
                    if ( v154 == (_QWORD *)qword_143A35788 && v153 == qword_143A35788 )
                    {
                      result = ((__int64 (__fastcall *)(_QWORD, __int64, __int64))unk_142F52DC0)(
                                 a1: *(_QWORD *)(qword_143A35A28 + 504),
                                 a2: v22,
                                 a3: v152);
                      if ( result != 0 )
                      {
                        v25 = (*(_QWORD *)v22)-- == 1;
                        if ( v25 )
                        {
                          v251 = result;
                          MEMORY[0x13B0039F0](a1: v22);
                          result = v251;
                        }
                        goto LABEL_308;
                      }
                      goto LABEL_563;
                    }
LABEL_302:
                    v155 = (__int64 (__fastcall **)(__int64, __int64))v154[12];
                    if ( v155 == nullptr )
                      goto LABEL_525;
                    v156 = v155[19];
                    if ( v156 == nullptr )
                    {
LABEL_430:
                      v185 = *v155;
                      if ( (_QWORD *)v153 == v154 )
                        goto LABEL_450;
                      goto LABEL_431;
                    }
LABEL_304:
                    result = v156(a1: v22, a2: v152);
                    if ( result != qword_143A35620 )
                      goto LABEL_305;
                    v25 = (*(_QWORD *)result)-- == 1;
                    if ( v25 )
                      MEMORY[0x13B0039F0](a1: result);
                    v155 = (__int64 (__fastcall **)(__int64, __int64))v154[12];
                    if ( v155 == nullptr )
                    {
LABEL_525:
                      if ( (_QWORD *)v153 == v154 )
                        goto LABEL_447;
                      goto LABEL_526;
                    }
                    goto LABEL_430;
                  }
                  if ( v153 == qword_143A354B8 )
                  {
                    v219 = *(double *)(v152 + 16);
                    v220 = *(double *)(v22 + 16);
                    --*(_QWORD *)v22;
                    v221 = v220 + v219;
                    result = ((__int64 (__fastcall *)(_QWORD))unk_1430DB3D0)(a1: *(_QWORD *)(*(_QWORD *)(qword_143A35A28 + 504)
                                                                                           + 16LL));
                    *(double *)(result + 16) = v221;
LABEL_308:
                    v25 = (*(_QWORD *)v152)-- == 1;
                    if ( v25 )
                    {
                      v241 = result;
                      (*(void (__fastcall **)(__int64))(*(_QWORD *)(v152 + 8) + 48LL))(a1: v152);
                      result = v241;
                    }
                    goto LABEL_70;
                  }
                  goto LABEL_538;
                }
                if ( v154 == (_QWORD *)qword_143A35788 )
                {
                  if ( (*(_BYTE *)(v22 + 32) & 3) == 0 )
                  {
                    if ( (_QWORD *)v153 != v154 )
                      goto LABEL_302;
                    if ( *(_QWORD *)(v152 + 16) != 0 )
                    {
                      v214 = ((__int64 (__fastcall *)(_QWORD, __int64 *, __int64))unk_142F5A1C0)(
                               a1: *(_QWORD *)(qword_143A35A28 + 504),
                               a2: &a7,
                               a3: v152);
                      goto LABEL_540;
                    }
LABEL_568:
                    v25 = (*(_QWORD *)v152)-- == 1;
                    if ( v25 )
                      (*(void (__fastcall **)(__int64))(v153 + 48))(a1: v152);
LABEL_336:
                    result = v22;
LABEL_70:
                    v56 = a1[7];
                    v57 = *(_QWORD *)(v56 + 8);
                    v58 = *(_QWORD *)(v57 + 40);
                    *(_QWORD *)(v56 + 8) = *(_QWORD *)(v57 + 48);
                    v59 = *(_QWORD **)(v58 + 16);
                    *(_DWORD *)(v58 + 64) = -1;
                    if ( v59 != nullptr )
                    {
                      *(_QWORD *)(v58 + 16) = 0;
                      v25 = (*v59)-- == 1;
                      if ( v25 )
                      {
                        v226 = result;
                        (*(void (**)(void))(v59[1] + 48LL))();
                        result = v226;
                      }
                    }
                    v25 = (*(_QWORD *)v58)-- == 1;
                    if ( v25 )
                    {
                      v227 = result;
                      (*(void (__fastcall **)(__int64))(*(_QWORD *)(v58 + 8) + 48LL))(a1: v58);
                      result = v227;
                    }
                    v25 = *(_QWORD *)result == 0;
                    *(_QWORD *)(v58 + 120) = 0;
                    if ( v25 )
                    {
                      v228 = result;
                      (*(void (__fastcall **)(__int64))(*(_QWORD *)(result + 8) + 48LL))(a1: result);
                      result = v228;
                    }
                    v25 = (*v14)-- == 1;
                    if ( v25 )
                    {
                      v229 = result;
                      (*(void (__fastcall **)(_QWORD *))(v14[1] + 48LL))(a1: v14);
                      return v229;
                    }
                    return result;
                  }
                  if ( (_QWORD *)v153 != v154 )
                    goto LABEL_302;
                }
                else if ( (_QWORD *)v153 != v154 )
                {
                  v196 = (__int64 (__fastcall **)(__int64, __int64))v154[12];
                  if ( v196 == nullptr )
                  {
LABEL_526:
                    v212 = *(__int64 (__fastcall ***)(__int64, __int64))(v153 + 96);
                    if ( v212 != nullptr )
                    {
                      v187 = *v212;
                      if ( *v212 == nullptr )
                        goto LABEL_447;
LABEL_444:
                      result = v187(a1: v22, a2: v152);
                      if ( result != qword_143A35620 )
                        goto LABEL_305;
                      v25 = (*(_QWORD *)result)-- == 1;
                      if ( v25 )
                        MEMORY[0x13B0039F0](a1: result);
                    }
LABEL_447:
                    v192 = v154[13];
                    if ( v192 == 0
                      || (v164 = *(__int64 (__fastcall **)(__int64, __int64))(v192 + 64)) == nullptr
                      && (v164 = *(__int64 (__fastcall **)(__int64, __int64))(v192 + 8)) == nullptr )
                    {
                      qword_143A358D8(a1: *(_QWORD *)qword_143A35450, a2: &unk_14359FE68, a3: v154[3]);
                      v25 = (*(_QWORD *)v152)-- == 1;
                      if ( v25 )
LABEL_351:
                        (*(void (__fastcall **)(__int64))(*(_QWORD *)(v152 + 8) + 48LL))(a1: v152);
LABEL_352:
                      v60 = a1[14];
                      a1[14] = 0;
                      v61 = (_QWORD *)a1[12];
                      v62 = a1[13];
                      *((_OWORD *)a1 + 6) = 0;
LABEL_353:
                      v63 = 116;
                      goto LABEL_91;
                    }
                    result = v164(a1: v22, a2: v152);
LABEL_305:
                    if ( result != 0 )
                    {
                      v25 = (*(_QWORD *)v22)-- == 1;
                      if ( v25 )
                      {
                        v240 = result;
                        (*(void (__fastcall **)(__int64))(*(_QWORD *)(v22 + 8) + 48LL))(a1: v22);
                        result = v240;
                      }
                      goto LABEL_308;
                    }
LABEL_563:
                    v25 = (*(_QWORD *)v152)-- == 1;
                    if ( !v25 )
                      goto LABEL_352;
                    goto LABEL_351;
                  }
                  v156 = v196[19];
                  if ( v156 == nullptr )
                  {
                    v185 = *v196;
LABEL_431:
                    v186 = *(__int64 (__fastcall ***)(__int64, __int64))(v153 + 96);
                    if ( v186 != nullptr )
                    {
                      v187 = *v186;
                      if ( *v186 != v185 )
                      {
                        if ( v185 == nullptr )
                          goto LABEL_443;
                        v188 = (_QWORD *)qword_143A35620;
                        if ( v187 == nullptr )
                          goto LABEL_439;
                        v252 = v185;
                        v247 = *v186;
                        v189 = ((__int64 (__fastcall *)(__int64, _QWORD *))unk_1430DB000)(a1: v153, a2: v154);
                        v190 = v247;
                        v185 = v252;
                        if ( v189 != 0 )
                        {
                          result = v247(a1: v22, a2: v152);
                          v188 = (_QWORD *)qword_143A35620;
                          if ( result != qword_143A35620 )
                            goto LABEL_305;
                          v25 = (*(_QWORD *)qword_143A35620)-- == 1;
                          v185 = v252;
                          if ( v25 )
                          {
                            MEMORY[0x13B0039F0](a1: qword_143A35620);
                            v185 = v252;
                          }
LABEL_439:
                          v190 = nullptr;
LABEL_440:
                          v248 = v190;
                          result = v185(a1: v22, a2: v152);
                          if ( (_QWORD *)result != v188 )
                            goto LABEL_305;
                          v25 = (*v188)-- == 1;
                          v187 = v248;
                          if ( v25 )
                          {
                            MEMORY[0x13B0039F0](a1: v188, a2: v191, a3: v248);
                            v187 = v248;
                          }
LABEL_443:
                          if ( v187 == nullptr )
                            goto LABEL_447;
                          goto LABEL_444;
                        }
LABEL_452:
                        v188 = (_QWORD *)qword_143A35620;
                        goto LABEL_440;
                      }
                    }
LABEL_450:
                    if ( v185 == nullptr )
                      goto LABEL_447;
                    v190 = nullptr;
                    goto LABEL_452;
                  }
                  goto LABEL_304;
                }
                if ( v153 != qword_143A354B8 )
                {
LABEL_538:
                  if ( v153 != qword_143A35560 )
                    goto LABEL_300;
                  v214 = ((__int64 (__fastcall *)(__int64 *, __int64))unk_1430E28C0)(a1: &a7, a2: v152);
LABEL_540:
                  v25 = (*(_QWORD *)v152)-- == 1;
                  if ( v25 )
                    (*(void (__fastcall **)(__int64))(*(_QWORD *)(v152 + 8) + 48LL))(a1: v152);
                  if ( v214 != 0 )
                    goto LABEL_319;
                  goto LABEL_352;
                }
                *(double *)(v22 + 16) = *(double *)(v22 + 16) + *(double *)(v152 + 16);
                goto LABEL_568;
              }
LABEL_310:
              v61 = (_QWORD *)a1[12];
              v62 = a1[13];
              v63 = 115;
              v60 = a1[14];
              *((_OWORD *)a1 + 6) = 0;
              a1[14] = 0;
              goto LABEL_91;
            }
            ((void (__fastcall *)(_QWORD *, _QWORD **, __int64))unk_142F6E530)(a1, a2: &a8, a3: qword_14393F780);
            v61 = a8;
            v62 = a9;
            v63 = 115;
            v60 = a10;
            v25 = (*v26)-- == 1;
            if ( !v25 )
              goto LABEL_91;
LABEL_90:
            v230 = v63;
            (*(void (__fastcall **)(_QWORD *))(v26[1] + 48LL))(a1: v26);
            v63 = v230;
            goto LABEL_91;
          }
          a7 = v22;
          v118 = ((__int64 (*)(void))unk_143219930)();
          if ( v118 == 0 )
          {
            ((void (__fastcall *)(_QWORD *, _QWORD **, __int64))unk_142F6E530)(a1, a2: &a8, a3: qword_14393F718);
            v61 = a8;
            v62 = a9;
            v63 = 112;
            v60 = a10;
            goto LABEL_91;
          }
          *(_DWORD *)(v13 + 40) = 112;
          v119 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64))unk_142F78640)(a1, a2: v118, a3: qword_14393F768);
          v120 = (_QWORD *)v119;
          if ( v119 == 0 )
            goto LABEL_238;
          v121 = ((__int64 (__fastcall *)(__int64, __int64))unk_1430EC890)(a1: v119, a2: qword_14393F728);
          v25 = (*v120)-- == 1;
          v48 = (_QWORD *)v121;
          if ( v25 )
            (*(void (__fastcall **)(_QWORD *))(v120[1] + 48LL))(a1: v120);
          if ( v48 == nullptr )
            goto LABEL_238;
          *(_DWORD *)(v13 + 40) = 113;
          v122 = ((__int64 (__fastcall *)(_QWORD *, _QWORD *, __int64))unk_1430D8EF0)(a1, a2: v14, a3: qword_14393F770);
          if ( v122 == 0 )
          {
            v61 = (_QWORD *)a1[12];
            v62 = a1[13];
            v63 = 113;
            v60 = a1[14];
            *((_OWORD *)a1 + 6) = 0;
            a1[14] = 0;
            v25 = (*v48)-- == 1;
            if ( !v25 )
              goto LABEL_91;
LABEL_344:
            v242 = v63;
            MEMORY[0x13B0039F0](a1: v48);
            v63 = v242;
            goto LABEL_91;
          }
          v237 = (_QWORD *)v122;
          v123 = ((__int64 (__fastcall *)(_QWORD *, __int64))unk_1430EC890)(a1: v14, a2: qword_14393F688);
          v124 = v237;
          v125 = (_QWORD *)v123;
          if ( v123 != 0 )
          {
            *(_DWORD *)(v13 + 40) = 112;
            a8 = v237;
            a9 = v123;
            v126 = ((__int64 (__fastcall *)(_QWORD *, _QWORD *, _QWORD **, __int64))unk_1430D4C80)(
                     a1,
                     a2: v48,
                     a3: &a8,
                     a4: qword_14393F778);
            v25 = (*v48)-- == 1;
            v127 = v237;
            v88 = v126;
            if ( v25 )
            {
              (*(void (__fastcall **)(_QWORD *))(v48[1] + 48LL))(a1: v48);
              v127 = v237;
            }
            v25 = (*v127)-- == 1;
            if ( v25 )
              (*(void (__fastcall **)(_QWORD *))(v127[1] + 48LL))(a1: v127);
            v25 = (*v125)-- == 1;
            if ( v25 )
              (*(void (__fastcall **)(_QWORD *))(v125[1] + 48LL))(a1: v125);
            if ( v88 == 0 )
              goto LABEL_238;
            v89 = *(_QWORD *)v22;
            v91 = *(_QWORD *)(v88 + 8);
            v128 = *(_QWORD **)(v22 + 8);
            if ( *(_QWORD *)v22 != 1 )
            {
              if ( (_QWORD *)v91 != v128 )
                goto LABEL_230;
              if ( v91 != qword_143A354B8 )
              {
LABEL_458:
                if ( v91 != qword_143A35560 )
                {
LABEL_230:
                  if ( v128 != (_QWORD *)qword_143A35788 || v91 != qword_143A35788 )
                    goto LABEL_232;
                  result = ((__int64 (__fastcall *)(_QWORD, __int64, __int64))unk_142F52DC0)(
                             a1: *(_QWORD *)(qword_143A35A28 + 504),
                             a2: v22,
                             a3: v88);
                  if ( result == 0 )
                  {
LABEL_236:
                    v25 = (*(_QWORD *)v88)-- == 1;
                    if ( v25 )
LABEL_237:
                      (*(void (__fastcall **)(__int64))(*(_QWORD *)(v88 + 8) + 48LL))(a1: v88);
LABEL_238:
                    v61 = (_QWORD *)a1[12];
                    v62 = a1[13];
                    v63 = 112;
                    v60 = a1[14];
                    *((_OWORD *)a1 + 6) = 0;
                    a1[14] = 0;
                    goto LABEL_91;
                  }
LABEL_428:
                  v25 = (*(_QWORD *)v22)-- == 1;
                  if ( v25 )
                  {
                    v246 = result;
                    MEMORY[0x13B0039F0](a1: v22);
                    result = v246;
                  }
                  goto LABEL_142;
                }
                v194 = ((__int64 (__fastcall *)(__int64 *, __int64))unk_1430E28C0)(a1: &a7, a2: v88);
LABEL_460:
                v25 = (*(_QWORD *)v88)-- == 1;
                if ( v25 )
                  (*(void (__fastcall **)(__int64))(*(_QWORD *)(v88 + 8) + 48LL))(a1: v88);
                if ( v194 != 0 )
                  goto LABEL_319;
                goto LABEL_238;
              }
              goto LABEL_534;
            }
            if ( v128 != (_QWORD *)qword_143A35788 )
            {
              if ( (_QWORD *)v91 != v128 )
              {
                v175 = (__int64 (__fastcall **)(__int64, __int64))v128[12];
                if ( v175 == nullptr )
                {
LABEL_454:
                  v193 = *(__int64 (__fastcall ***)(__int64, __int64))(v91 + 96);
                  if ( v193 != nullptr )
                  {
                    v167 = *v193;
                    if ( *v193 == nullptr )
                      goto LABEL_387;
LABEL_384:
                    result = v167(a1: v22, a2: v88);
                    if ( result != qword_143A35620 )
                      goto LABEL_235;
                    v25 = (*(_QWORD *)result)-- == 1;
                    if ( v25 )
                      MEMORY[0x13B0039F0](a1: result);
                  }
LABEL_387:
                  v173 = v128[13];
                  if ( v173 == 0
                    || (v174 = *(__int64 (__fastcall **)(__int64, __int64))(v173 + 64)) == nullptr
                    && (v174 = *(__int64 (__fastcall **)(__int64, __int64))(v173 + 8)) == nullptr )
                  {
                    qword_143A358D8(a1: *(_QWORD *)qword_143A35450, a2: &unk_14359FE68, a3: v128[3]);
                    v25 = (*(_QWORD *)v88)-- == 1;
                    if ( !v25 )
                      goto LABEL_238;
                    goto LABEL_237;
                  }
                  result = v174(a1: v22, a2: v88);
LABEL_235:
                  if ( result == 0 )
                    goto LABEL_236;
                  goto LABEL_140;
                }
                v130 = v175[19];
                if ( v130 == nullptr )
                {
                  v165 = *v175;
LABEL_367:
                  v166 = *(__int64 (__fastcall ***)(__int64, __int64))(v91 + 96);
                  if ( v166 != nullptr )
                  {
                    v167 = *v166;
                    if ( *v166 != v165 )
                    {
                      if ( v165 == nullptr )
                        goto LABEL_383;
                      v168 = (_QWORD *)qword_143A35620;
                      if ( v167 != nullptr )
                      {
                        v169 = *(_QWORD *)(v91 + 344);
                        if ( v169 != 0 )
                        {
                          v170 = *(_QWORD *)(v169 + 16);
                          v171 = 0;
                          if ( v170 <= 0 )
                          {
LABEL_392:
                            v168 = (_QWORD *)qword_143A35620;
                            goto LABEL_380;
                          }
                          while ( *(_QWORD **)(v169 + 8 * v171 + 24) != v128 )
                          {
                            if ( v170 == ++v171 )
                              goto LABEL_392;
                          }
                        }
                        else
                        {
                          v222 = (_QWORD *)v91;
                          while ( v222 != v128 )
                          {
                            v222 = (_QWORD *)v222[32];
                            if ( v222 == nullptr )
                            {
                              if ( v128 == (_QWORD *)qword_143A35760 )
                                break;
                              goto LABEL_392;
                            }
                          }
                        }
                        v243 = v165;
                        result = v167(a1: v22, a2: v88);
                        v168 = (_QWORD *)qword_143A35620;
                        if ( result != qword_143A35620 )
                          goto LABEL_235;
                        v25 = (*(_QWORD *)qword_143A35620)-- == 1;
                        v165 = v243;
                        if ( v25 )
                        {
                          MEMORY[0x13B0039F0](a1: qword_143A35620);
                          v165 = v243;
                        }
                      }
                      v167 = nullptr;
LABEL_380:
                      v244 = v167;
                      result = v165(a1: v22, a2: v88);
                      if ( (_QWORD *)result != v168 )
                        goto LABEL_235;
                      v25 = (*v168)-- == 1;
                      v167 = v244;
                      if ( v25 )
                      {
                        MEMORY[0x13B0039F0](a1: v168, a2: v172, a3: v244);
                        v167 = v244;
                      }
LABEL_383:
                      if ( v167 == nullptr )
                        goto LABEL_387;
                      goto LABEL_384;
                    }
                  }
LABEL_390:
                  if ( v165 == nullptr )
                    goto LABEL_387;
                  v167 = nullptr;
                  goto LABEL_392;
                }
                goto LABEL_234;
              }
LABEL_545:
              if ( v91 != qword_143A354B8 )
                goto LABEL_458;
              goto LABEL_333;
            }
            if ( (*(_BYTE *)(v22 + 32) & 3) != 0 )
            {
              if ( (_QWORD *)v91 == v128 )
                goto LABEL_545;
            }
            else if ( (_QWORD *)v91 == v128 )
            {
              if ( *(_QWORD *)(v88 + 16) != 0 )
              {
                v194 = ((__int64 (__fastcall *)(_QWORD, __int64 *, __int64))unk_142F5A1C0)(
                         a1: *(_QWORD *)(qword_143A35A28 + 504),
                         a2: &a7,
                         a3: v88);
                goto LABEL_460;
              }
LABEL_334:
              v25 = (*(_QWORD *)v88)-- == 1;
              if ( v25 )
                (*(void (__fastcall **)(__int64))(v91 + 48))(a1: v88);
              goto LABEL_336;
            }
LABEL_232:
            v129 = (__int64 (__fastcall **)(__int64, __int64))v128[12];
            if ( v129 == nullptr )
            {
LABEL_453:
              if ( (_QWORD *)v91 == v128 )
                goto LABEL_387;
              goto LABEL_454;
            }
            v130 = v129[19];
            if ( v130 == nullptr )
              goto LABEL_366;
LABEL_234:
            result = v130(a1: v22, a2: v88);
            if ( result != qword_143A35620 )
              goto LABEL_235;
            v25 = (*(_QWORD *)result)-- == 1;
            if ( v25 )
              MEMORY[0x13B0039F0](a1: result);
            v129 = (__int64 (__fastcall **)(__int64, __int64))v128[12];
            if ( v129 != nullptr )
            {
LABEL_366:
              v165 = *v129;
              if ( (_QWORD *)v91 == v128 )
                goto LABEL_390;
              goto LABEL_367;
            }
            goto LABEL_453;
          }
          v61 = (_QWORD *)a1[12];
          v62 = a1[13];
          v60 = a1[14];
          *((_OWORD *)a1 + 6) = 0;
          a1[14] = 0;
          v25 = (*v48)-- == 1;
          if ( v25 )
          {
            MEMORY[0x13B0039F0](a1: v48);
            v124 = v237;
          }
          v25 = (*v124)-- == 1;
          v63 = 113;
          if ( v25 )
          {
            MEMORY[0x13B0039F0](a1: v124);
            v63 = 113;
          }
LABEL_91:
          if ( v60 != 0 )
          {
LABEL_92:
            if ( *(_QWORD *)(v60 + 24) != v13 )
            {
              v71 = *(_QWORD *)qword_1435FA6C0;
              if ( *(_QWORD *)qword_1435FA6C0 != 0 )
              {
                *(_QWORD *)qword_1435FA6C0 = *(_QWORD *)v71;
                *(_QWORD *)v71 = 1;
                --*(_DWORD *)qword_1435FA6D0;
              }
              else
              {
                v231 = v63;
                v86 = MEMORY[0x13B00DD60](a1: qword_143A35A88);
                v63 = v231;
                v71 = v86;
              }
              *(_QWORD *)(v71 + 24) = v13;
              ++*(_QWORD *)v13;
              v72 = *(_QWORD *)(qword_143A35A28 + 504);
              *(_DWORD *)(v71 + 36) = v63;
              *(_DWORD *)(v71 + 32) = -1;
              v73 = *(_QWORD *)(*(_QWORD *)(v72 + 16) + 744LL);
              v74 = *(_QWORD *)(v73 + 8);
              *(_QWORD *)&v75 = v73;
              v76 = v74 | *(_QWORD *)(v71 - 8) & 3LL;
              *(_QWORD *)v74 = v71 - 16;
              *((_QWORD *)&v75 + 1) = v76;
              *(_OWORD *)(v71 - 16) = v75;
              v25 = *(_QWORD *)v60 == 0;
              *(_QWORD *)(v73 + 8) = v71 - 16;
              *(_QWORD *)(v71 + 16) = v60;
              if ( v25 )
                (*(void (__fastcall **)(__int64))(*(_QWORD *)(v60 + 8) + 48LL))(a1: v60);
              v60 = v71;
            }
            goto LABEL_98;
          }
LABEL_81:
          v60 = *(_QWORD *)qword_1435FA6C0;
          if ( *(_QWORD *)qword_1435FA6C0 != 0 )
          {
            *(_QWORD *)qword_1435FA6C0 = *(_QWORD *)v60;
            *(_QWORD *)v60 = 1;
            --*(_DWORD *)qword_1435FA6D0;
          }
          else
          {
            v236 = v63;
            v110 = MEMORY[0x13B00DD60](a1: qword_143A35A88);
            v63 = v236;
            v60 = v110;
          }
          *(_QWORD *)(v60 + 16) = 0;
          *(_QWORD *)(v60 + 24) = v13;
          ++*(_QWORD *)v13;
          v64 = *(_QWORD *)(qword_143A35A28 + 504);
          *(_DWORD *)(v60 + 36) = v63;
          v65 = *(_QWORD *)(v64 + 16);
          *(_DWORD *)(v60 + 32) = -1;
          v66 = *(_QWORD *)(v65 + 744);
          v67 = *(_QWORD *)(v66 + 8);
          *(_QWORD *)&v68 = v66;
          v69 = v67 | *(_QWORD *)(v60 - 8) & 3LL;
          *(_QWORD *)v67 = v60 - 16;
          *((_QWORD *)&v68 + 1) = v69;
          *(_OWORD *)(v60 - 16) = v68;
          *(_QWORD *)(v66 + 8) = v60 - 16;
LABEL_98:
          ((void (__fastcall *)(__int64, void *, _QWORD *, __int64))unk_142F544C0)(
            a1: v13,
            a2: &unk_14359FC67,
            a3: v14,
            a4: v22);
          if ( qword_143943E38 == v13 )
          {
            v25 = (*(_QWORD *)v13)-- == 1;
            if ( v25 )
              (*(void (__fastcall **)(__int64))(*(_QWORD *)(v13 + 8) + 48LL))(a1: v13);
            qword_143943E38 = 0;
          }
          v77 = a1[7];
          v78 = *(_QWORD *)(v77 + 8);
          v79 = *(_QWORD *)(v78 + 40);
          v80 = *(_QWORD **)(v79 + 16);
          *(_QWORD *)(v77 + 8) = *(_QWORD *)(v78 + 48);
          *(_DWORD *)(v79 + 64) = -1;
          if ( v80 != nullptr )
          {
            *(_QWORD *)(v79 + 16) = 0;
            v25 = (*v80)-- == 1;
            if ( v25 )
              (*(void (**)(void))(v80[1] + 48LL))();
          }
          v25 = (*(_QWORD *)v79)-- == 1;
          if ( v25 )
            (*(void (__fastcall **)(__int64))(*(_QWORD *)(v79 + 8) + 48LL))(a1: v79);
          *(_QWORD *)(v79 + 120) = 0;
          if ( v22 != 0 )
          {
            v25 = (*(_QWORD *)v22)-- == 1;
            if ( v25 )
              (*(void (__fastcall **)(__int64))(*(_QWORD *)(v22 + 8) + 48LL))(a1: v22);
          }
          v25 = (*v14)-- == 1;
          if ( v25 )
            (*(void (__fastcall **)(_QWORD *))(v14[1] + 48LL))(a1: v14);
          MEMORY[0x13B00DF80](a1, a2: v61, a3: v62, a4: v60);
          return 0;
        }
      }
      v61 = (_QWORD *)a1[12];
      v62 = a1[13];
      v63 = 111;
      v60 = a1[14];
      *((_OWORD *)a1 + 6) = 0;
      a1[14] = 0;
      goto LABEL_91;
    }
  }
  v61 = (_QWORD *)a1[12];
  v62 = a1[13];
  v63 = 109;
  v60 = a1[14];
  *((_OWORD *)a1 + 6) = 0;
  a1[14] = 0;
  goto LABEL_91;
}