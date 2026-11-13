// local variable allocation has failed, the output may be wrong!
// write access to const memory has been detected, the output may be wrong!
_QWORD *__fastcall sub_1406BCBF0(
        _QWORD *a1,
        __int64 a2,
        __int64 **a3,
        __int64 a4,
        __int64 a5,
        __int64 a6,
        __int64 a7,
        __int64 a8,
        __int64 a9,
        __int64 a10,
        __int64 a11,
        __int64 a12,
        __int64 a13,
        __int64 a14,
        __int64 a15,
        __int64 a16,
        __int64 a17,
        __int64 a18,
        __int64 a19,
        __int64 a20,
        __int64 a21,
        __int64 a22,
        __int64 a23,
        __int64 a24,
        __int64 a25,
        __int64 a26,
        __int64 a27,
        __int64 a28,
        __int64 a29,
        __int64 a30,
        __int64 a31,
        __int64 a32,
        __int64 a33,
        __int64 a34,
        __int64 *a35,
        _QWORD *a36,
        __int64 a37,
        __int64 a38,
        __int64 a39,
        __int64 a40,
        __int64 a41,
        __int64 a42,
        __int64 a43,
        __int64 a44,
        __int64 a45,
        __int64 a46,
        __int64 a47,
        __int64 a48,
        __int64 a49,
        __int64 a50,
        __int64 a51,
        __int64 a52,
        __int64 a53,
        __int64 a54,
        __int64 a55,
        __int64 a56,
        __int64 a57,
        __int64 a58,
        __int64 a59,
        __int64 a60,
        __int64 a61,
        _QWORD *a62,
        _QWORD *a63,
        __int64 a64)
{
  _QWORD *v64; // rbp
  _QWORD *v65; // r13
  _QWORD *v66; // r14
  _QWORD *v67; // r15
  __int64 v68; // rbx
  __int64 v70; // rax
  __int64 v71; // rdx
  __int64 v72; // rax
  __int64 v73; // rdx
  _QWORD *v74; // rax
  _QWORD *v75; // rdi
  unsigned __int64 v76; // rax
  _QWORD *v77; // rdx
  __int64 v78; // rax
  __int64 v79; // rcx
  bool v80; // zf
  _QWORD *v81; // rax
  __int64 v82; // rax
  __int64 v83; // rax
  __int64 v84; // rax
  __int64 v85; // rax
  __int64 v86; // rax
  __int64 v87; // rax
  __int64 v88; // rax
  __int64 v89; // rax
  __int64 v90; // rax
  __int64 v91; // rax
  _QWORD *v92; // rdx
  __int64 v93; // rax
  __int64 v94; // rax
  _QWORD *v95; // rdx
  __int64 v96; // rax
  __int64 v97; // rax
  _QWORD *v98; // rdx
  __int64 v99; // rax
  __int64 v100; // rax
  _QWORD *v101; // rdx
  __int64 v102; // rax
  __int64 v103; // rax
  _QWORD *v104; // rdx
  __int64 v105; // rax
  __int64 v106; // rax
  _QWORD *v107; // rdx
  __int64 v108; // rax
  __int64 v109; // rax
  __int64 v110; // rax
  _QWORD *v111; // rdx
  __int64 v112; // rax
  __int64 v113; // rax
  _QWORD *v114; // rdx
  __int64 v115; // rax
  _QWORD *v116; // rdx
  __int64 v117; // rax
  __int64 v118; // rax
  _QWORD *v119; // rdx
  __int64 v120; // rax
  __int64 v121; // rax
  __int64 v122; // rax
  int v123; // eax
  __int64 v124; // rax
  _QWORD *v125; // r8
  __int64 v126; // rcx
  __int64 (__fastcall *v127)(__int64, __int64); // rax
  __int64 v128; // rax
  _QWORD *v129; // r9
  __int64 v130; // rdx
  __int64 (__fastcall *v131)(_QWORD *, _QWORD *, _QWORD *); // rax
  _QWORD *v132; // r8
  __int64 v133; // rax
  _QWORD *v134; // r9
  _QWORD *v135; // rdx
  __int64 v136; // rcx
  _QWORD *v137; // r12
  int v138; // r12d
  __int64 v139; // rax
  __int64 v140; // rax
  __int64 v141; // rax
  __int64 v142; // rax
  char v143; // r12
  _QWORD *v144; // rdx
  __int64 v145; // r8
  __int64 v146; // r9
  int v147; // eax
  __int64 v148; // rax
  __int64 v149; // r12
  __int64 v150; // rdx
  __int64 v151; // rax
  _QWORD *v152; // r12
  __int64 v153; // rax
  __int64 v154; // rdx
  _QWORD *v155; // r8
  _QWORD *v156; // r12
  __int64 v157; // rcx
  __int64 v158; // rax
  _QWORD *v159; // r12
  __int64 v160; // rax
  _QWORD *result; // rax
  __int64 v162; // rdx
  __int64 v163; // rdx
  __int64 v164; // rdx
  __int64 v165; // rdx
  __int64 v166; // rdx
  __int64 v167; // rdx
  __int64 v168; // rdx
  __int64 v169; // rdx
  __int64 v170; // rdx
  __int64 v171; // rdx
  __int64 v172; // rdx
  __int64 v173; // rdx
  __int64 v174; // rdx
  __int64 v175; // rdx
  __int64 v176; // rdx
  __int64 v177; // rdx
  __int64 v178; // rdx
  __int64 v179; // rdx
  __int64 v180; // rdx
  __int64 v181; // rdx
  __int64 v182; // rdx
  __int64 v183; // rdx
  __int64 v184; // rdx
  __int64 v185; // rdx
  __int64 *v186; // rsi
  __int64 v187; // rdx
  __int64 v188; // rax
  _QWORD *v189; // rax
  __int64 v190; // r12
  int v191; // edx
  __int64 v192; // rax
  __int64 v193; // rcx
  unsigned __int64 v194; // r9
  __int128 v195; // xmm0
  __int64 v196; // rdx
  __int64 v197; // rax
  __int64 v198; // rdx
  __int64 v199; // rbx
  _QWORD *v200; // rcx
  __int64 *v201; // rbx
  __int64 *v202; // rdi
  __int64 *v203; // rcx
  _QWORD *v204; // rax
  __int64 v205; // rax
  __int64 v206; // rdx
  unsigned __int64 v207; // r8
  __int128 v208; // xmm0
  __int64 v209; // rax
  _QWORD *v210; // rax
  _QWORD *v211; // rax
  _QWORD *v212; // rax
  _QWORD *v213; // rax
  _QWORD *v214; // rax
  _QWORD *v215; // rax
  _QWORD *v216; // rax
  _QWORD *v217; // rax
  _QWORD *v218; // rax
  _QWORD *v219; // rax
  _QWORD *v220; // rax
  __int64 v221; // rax
  _QWORD *v222; // rax
  _QWORD *v223; // rax
  _QWORD *v224; // rax
  _QWORD *v225; // rax
  _QWORD *v226; // rax
  _QWORD *v227; // rax
  _QWORD *v228; // rax
  _QWORD *v229; // rax
  _QWORD *v230; // rax
  _QWORD *v231; // rax
  _QWORD *v232; // rax
  _QWORD *v233; // rax
  _QWORD *v234; // rax
  _QWORD *v235; // rax
  _QWORD *v236; // rax
  _QWORD *v237; // rax
  _QWORD *v238; // rax
  _QWORD *v239; // rax
  _QWORD *v240; // rax
  _QWORD *v241; // rax
  _QWORD *v242; // rax
  _QWORD *v243; // rax
  _QWORD *v244; // rax
  _QWORD *v245; // rax
  _QWORD *v246; // rax
  _QWORD *v247; // rax
  _QWORD *v248; // rax
  _QWORD *v249; // rax
  _QWORD *v250; // rax
  _QWORD *v251; // rax
  _QWORD *v252; // rax
  _QWORD *v253; // rax
  _QWORD *v254; // rax
  _QWORD *v255; // rax
  __int64 v256; // rax
  __int64 *v257; // rax
  __int64 *v258; // rax
  _QWORD *v259; // rax
  _QWORD *v260; // rax
  _QWORD *v261; // rax
  _QWORD *v262; // rax
  __int64 v263; // r10
  int v264; // eax
  __int64 v265; // rax
  int v266; // eax
  __int64 *v267; // rax
  __int64 v268; // rdx
  _QWORD *v269; // rax
  _QWORD *v270; // rax
  _QWORD *v271; // rax
  __int64 v272; // rax
  _QWORD *v273; // rax
  _QWORD *v274; // rax
  _QWORD *v275; // rax
  _QWORD *v276; // rax
  _QWORD *v277; // rax
  _QWORD *v278; // rax
  _QWORD *v279; // rax
  _QWORD *v280; // r9
  _QWORD *v281; // rax
  _QWORD *v282; // rax
  _QWORD *v283; // rax
  __int64 v284; // rax
  _QWORD *v285; // r12
  _QWORD *v286; // rax
  _QWORD *v287; // rax
  _QWORD *v288; // rdx
  _QWORD *v289; // rdx
  _QWORD *v290; // rax
  _QWORD *v291; // rdx
  _QWORD *v292; // rax
  _QWORD *v293; // rax
  _QWORD *v294; // rax
  _QWORD *v295; // rax
  __int64 (__fastcall *v296)(_QWORD *, __int64); // r9
  __int64 v297; // rdx
  __int64 v298; // rax
  __int64 *v299; // [rsp+408h] [rbp+110h]
  _QWORD *v300; // [rsp+408h] [rbp+110h]
  __int64 v301; // [rsp+408h] [rbp+110h]
  _QWORD *v302; // [rsp+410h] [rbp+118h]
  _QWORD *v303; // [rsp+410h] [rbp+118h]
  _QWORD *v304; // [rsp+410h] [rbp+118h]
  _QWORD *v305; // [rsp+410h] [rbp+118h]
  _QWORD *v306; // [rsp+410h] [rbp+118h]
  _QWORD *v307; // [rsp+410h] [rbp+118h]
  _QWORD *v308; // [rsp+410h] [rbp+118h]
  _QWORD *v309; // [rsp+410h] [rbp+118h]
  _QWORD *v310; // [rsp+410h] [rbp+118h]
  _QWORD *v311; // [rsp+410h] [rbp+118h]
  _QWORD *v312; // [rsp+410h] [rbp+118h]
  _QWORD *v313; // [rsp+410h] [rbp+118h]
  _QWORD *v314; // [rsp+410h] [rbp+118h]
  _QWORD *v315; // [rsp+410h] [rbp+118h]
  _QWORD *v316; // [rsp+410h] [rbp+118h]
  _QWORD *v317; // [rsp+410h] [rbp+118h]
  _QWORD *v318; // [rsp+410h] [rbp+118h]
  _QWORD *v319; // [rsp+410h] [rbp+118h]
  _QWORD *v320; // [rsp+410h] [rbp+118h]
  _QWORD *v321; // [rsp+410h] [rbp+118h]
  _QWORD *v322; // [rsp+410h] [rbp+118h]
  _QWORD *v323; // [rsp+410h] [rbp+118h]
  _QWORD *v324; // [rsp+410h] [rbp+118h]
  _QWORD *v325; // [rsp+410h] [rbp+118h]
  _QWORD *v326; // [rsp+410h] [rbp+118h]
  _QWORD *v327; // [rsp+410h] [rbp+118h]
  _QWORD *v328; // [rsp+410h] [rbp+118h]
  _QWORD *v329; // [rsp+410h] [rbp+118h]
  _QWORD *v330; // [rsp+410h] [rbp+118h]
  __int64 v331; // [rsp+410h] [rbp+118h]
  __int64 v332; // [rsp+418h] [rbp+120h]
  _QWORD *v333; // [rsp+420h] [rbp+128h]
  __int64 v334; // [rsp+420h] [rbp+128h]
  _QWORD *v335; // [rsp+428h] [rbp+130h]
  __int64 v336; // [rsp+428h] [rbp+130h]
  _QWORD *v337; // [rsp+430h] [rbp+138h]
  __int64 v338; // [rsp+430h] [rbp+138h]
  _QWORD *v339; // [rsp+438h] [rbp+140h]
  __int64 v340; // [rsp+438h] [rbp+140h]
  _QWORD *v341; // [rsp+440h] [rbp+148h]
  __int64 v342; // [rsp+440h] [rbp+148h]
  _QWORD *v343; // [rsp+448h] [rbp+150h]
  __int64 v344; // [rsp+448h] [rbp+150h]
  __int64 v345; // [rsp+448h] [rbp+150h]
  _QWORD *v346; // [rsp+450h] [rbp+158h]
  _QWORD *v347; // [rsp+458h] [rbp+160h]
  __int64 v348; // [rsp+458h] [rbp+160h]
  __int64 v349; // [rsp+458h] [rbp+160h]
  _QWORD *v350; // [rsp+460h] [rbp+168h]
  _QWORD *v351; // [rsp+460h] [rbp+168h]
  __int64 v352; // [rsp+460h] [rbp+168h]
  _QWORD *v353; // [rsp+460h] [rbp+168h]
  _QWORD *v354; // [rsp+460h] [rbp+168h]
  __int64 v355; // [rsp+460h] [rbp+168h]
  __int64 v356; // [rsp+460h] [rbp+168h]
  __int64 v357; // [rsp+460h] [rbp+168h]
  __int64 v358; // [rsp+460h] [rbp+168h]
  __int64 v359; // [rsp+460h] [rbp+168h]
  __int64 v360; // [rsp+460h] [rbp+168h]
  _QWORD *v361; // [rsp+460h] [rbp+168h]
  _QWORD *v362; // [rsp+468h] [rbp+170h]
  __int64 *v363; // [rsp+470h] [rbp+178h]
  _QWORD *v364; // [rsp+478h] [rbp+180h]
  _QWORD *v365; // [rsp+480h] [rbp+188h]
  __int64 *v366; // [rsp+488h] [rbp+190h]
  __int64 *v367; // [rsp+490h] [rbp+198h]
  __int64 *v368; // [rsp+498h] [rbp+1A0h]
  __int64 *v369; // [rsp+4A0h] [rbp+1A8h]
  __int64 *v370; // [rsp+4A8h] [rbp+1B0h]
  _QWORD *v371; // [rsp+4B0h] [rbp+1B8h]
  __int64 *v372; // [rsp+4B8h] [rbp+1C0h]
  __int64 *v373; // [rsp+4C0h] [rbp+1C8h]
  _QWORD *v374; // [rsp+4C8h] [rbp+1D0h]
  _QWORD *v375; // [rsp+4D0h] [rbp+1D8h]
  __int64 v376; // [rsp+4D0h] [rbp+1D8h]
  _QWORD *v377; // [rsp+4D0h] [rbp+1D8h]
  _QWORD *v378; // [rsp+4D0h] [rbp+1D8h]
  _QWORD *v379; // [rsp+4D8h] [rbp+1E0h]
  __int64 v380; // [rsp+4D8h] [rbp+1E0h]
  _QWORD *v381; // [rsp+4D8h] [rbp+1E0h]
  __int64 v382; // [rsp+4E0h] [rbp+1E8h]
  _QWORD *v383; // [rsp+4E0h] [rbp+1E8h]
  __int64 v384; // [rsp+4E0h] [rbp+1E8h]
  _QWORD *v385; // [rsp+4E0h] [rbp+1E8h]
  __int64 v386; // [rsp+4E0h] [rbp+1E8h]
  int v387; // [rsp+4E0h] [rbp+1E8h]
  int v388; // [rsp+4E0h] [rbp+1E8h]

  v68 = qword_143944148;
  v299 = *a3;
  if ( qword_143944148 == 0 )
    goto LABEL_4;
  v70 = *(_QWORD *)qword_143944148;
  if ( *(__int64 *)qword_143944148 > 1 )
  {
    *(_QWORD *)qword_143944148 = v70 - 1;
LABEL_4:
    qword_143944148 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64, __int64))unk_142F58E90)(
                        a1,
                        a2: qword_143944140,
                        a3: qword_143944160,
                        a4: 248);
    v68 = qword_143944148;
    goto LABEL_5;
  }
  if ( *(_QWORD *)(qword_143944148 + 16) != 0 )
  {
    v188 = v70 - 1;
    *(_QWORD *)qword_143944148 = v188;
    if ( v188 == 0 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(qword_143944148 + 8) + 48LL))(a1: qword_143944148);
    goto LABEL_4;
  }
LABEL_5:
  v71 = a1[7];
  v72 = *(_QWORD *)(v71 + 8);
  *(_QWORD *)(v68 + 120) = v72;
  *(_QWORD *)(v71 + 8) = v68 + 72;
  if ( v72 != 0
    && (*(_BYTE *)(v72 + 69) == 1
     || *(_QWORD *)(v72 + 56) >= (unsigned __int64)(*(_QWORD *)(v72 + 32)
                                                  + 2LL * *(int *)(*(_QWORD *)(v72 + 32) + 168LL)
                                                  + 184)) )
  {
    v73 = *(_QWORD *)(v68 + 112);
    if ( v73 != 0 )
    {
      v74 = *(_QWORD **)(v72 + 40);
      *(_QWORD *)(v73 + 16) = v74;
      if ( v74 != nullptr )
        ++*v74;
    }
  }
  ++*(_QWORD *)v68;
  *(_DWORD *)(v68 + 64) = 0;
  *(_DWORD *)(v68 + 40) = 26;
  a64 = qword_143A35618;
  v75 = (_QWORD *)qword_1435D24B0;
  STACK[0x500] = qword_14393FD50;
  v76 = *(_QWORD *)(qword_1435FA6E0 + 16);
  v77 = *(_QWORD **)qword_1435D24B0;
  *(__m128 *)&a62 = _mm_loadh_ps(qword_14393FD08);
  STACK[0x508] = v76;
  if ( v77 == nullptr )
  {
    v204 = (_QWORD *)qword_143A352E0(a1: *(_QWORD *)qword_1435FA560, a2: &unk_14359FC6A);
    v77 = v204;
    if ( v204 == nullptr )
    {
      qword_143A35A60(a1: 0);
      qword_143A35A30(a1: 1);
      goto LABEL_414;
    }
    ++*v204;
    *(_QWORD *)qword_1435D24B0 = v204;
  }
  v78 = ((__int64 (__fastcall *)(_QWORD *, _QWORD *, _QWORD **))unk_142F85F90)(a1, a2: v77, a3: &a62);
  v66 = (_QWORD *)v78;
  if ( v78 == 0 )
  {
    v211 = (_QWORD *)a1[12];
    v190 = a1[14];
    v65 = nullptr;
    a1[14] = 0;
    v67 = nullptr;
    v64 = nullptr;
    v75 = nullptr;
    v378 = v211;
    v191 = 26;
    v354 = nullptr;
    v381 = (_QWORD *)a1[13];
    v362 = nullptr;
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v346 = nullptr;
    v341 = nullptr;
    v339 = nullptr;
    v337 = nullptr;
    v335 = nullptr;
    v333 = nullptr;
    a36 = nullptr;
    a35 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v79 = *(_QWORD *)(v78 + 8);
  if ( v79 != qword_143A355C8 && (unsigned int)qword_143A35780(a1: v79, a2: qword_143A355C8) == 0 )
  {
    a35 = (__int64 *)qword_143A35660(a1: v66, a2: qword_14393FD58);
    if ( a35 == nullptr )
    {
      a35 = (__int64 *)((__int64 (__fastcall *)(_QWORD *, _QWORD *, __int64))unk_1430ECB60)(
                         a1,
                         a2: v66,
                         a3: qword_14393FD58);
      goto LABEL_398;
    }
LABEL_18:
    v80 = (*v66)-- == 1;
    if ( v80 )
      (*(void (__fastcall **)(_QWORD *))(v66[1] + 48LL))(a1: v66);
    goto LABEL_20;
  }
  a35 = (__int64 *)qword_143A35660(a1: v66, a2: qword_14393FD58);
  if ( a35 != nullptr )
    goto LABEL_18;
  a35 = (__int64 *)((__int64 (__fastcall *)(_QWORD *, _QWORD *, _QWORD, __int64))unk_1432AB760)(
                     a1,
                     a2: v66,
                     a3: *(_QWORD *)&qword_14393FD08[0],
                     a4: qword_14393FD58);
LABEL_398:
  v80 = (*v66)-- == 1;
  if ( v80 )
    (*(void (__fastcall **)(_QWORD *))(v66[1] + 48LL))(a1: v66);
  if ( a35 == nullptr )
  {
    v213 = (_QWORD *)a1[12];
    v190 = a1[14];
    v65 = nullptr;
    a1[14] = 0;
    v67 = nullptr;
    v64 = nullptr;
    v75 = nullptr;
    v378 = v213;
    v66 = nullptr;
    v191 = 26;
    v354 = nullptr;
    v381 = (_QWORD *)a1[13];
    v362 = nullptr;
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v346 = nullptr;
    v341 = nullptr;
    v339 = nullptr;
    v337 = nullptr;
    v335 = nullptr;
    v333 = nullptr;
    a36 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
LABEL_20:
  *(_DWORD *)(v68 + 40) = 28;
  v81 = (_QWORD *)((__int64 (__fastcall *)(_QWORD *, __int64 *))unk_142F69C20)(a1, a2: a35);
  v66 = v81;
  if ( v81 == nullptr )
  {
    v215 = (_QWORD *)a1[12];
    v190 = a1[14];
    v65 = nullptr;
    a1[14] = 0;
    v67 = nullptr;
    v64 = nullptr;
    v75 = nullptr;
    v378 = v215;
    v191 = 28;
    v354 = nullptr;
    v381 = (_QWORD *)a1[13];
    v362 = nullptr;
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v346 = nullptr;
    v341 = nullptr;
    v339 = nullptr;
    v337 = nullptr;
    v335 = nullptr;
    v333 = nullptr;
    a36 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v80 = (*v81)-- == 1;
  if ( v80 )
    (*(void (__fastcall **)(_QWORD *))(v81[1] + 48LL))(a1: v81);
  v82 = MEMORY[0x13B054620](a1, a2: v299, a3: qword_14393FD60);
  v75 = (_QWORD *)v82;
  if ( v82 == 0 )
  {
    v210 = (_QWORD *)a1[12];
    v190 = a1[14];
    v65 = nullptr;
    a1[14] = 0;
    v67 = nullptr;
    v64 = nullptr;
    v66 = nullptr;
    v378 = v210;
    v191 = 29;
    v354 = nullptr;
    v381 = (_QWORD *)a1[13];
    v362 = nullptr;
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v346 = nullptr;
    v341 = nullptr;
    v339 = nullptr;
    v337 = nullptr;
    v335 = nullptr;
    v333 = nullptr;
    a36 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v83 = MEMORY[0x13B054620](a1, a2: v82, a3: qword_14393FD68);
  v80 = (*v75)-- == 1;
  v66 = (_QWORD *)v83;
  if ( v80 )
    (*(void (__fastcall **)(_QWORD *))(v75[1] + 48LL))(a1: v75);
  if ( v66 == nullptr )
  {
    v189 = (_QWORD *)a1[12];
    v190 = a1[14];
    v65 = nullptr;
    a1[14] = 0;
    v67 = nullptr;
    v64 = nullptr;
    v75 = nullptr;
    v378 = v189;
    v191 = 29;
    v354 = nullptr;
    v381 = (_QWORD *)a1[13];
    v362 = nullptr;
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v346 = nullptr;
    v341 = nullptr;
    v339 = nullptr;
    v337 = nullptr;
    v335 = nullptr;
    v333 = nullptr;
    a36 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
LABEL_281:
    if ( v190 != 0 )
    {
      if ( *(_QWORD *)(v190 + 24) != v68 )
      {
        v192 = *(_QWORD *)qword_1435FA6C0;
        if ( *(_QWORD *)qword_1435FA6C0 != 0 )
        {
          *(_QWORD *)qword_1435FA6C0 = *(_QWORD *)v192;
          *(_QWORD *)v192 = 1;
          --*(_DWORD *)qword_1435FA6D0;
        }
        else
        {
          v387 = v191;
          v192 = MEMORY[0x13B00DD60](a1: qword_143A35A88);
          v191 = v387;
        }
        *(_QWORD *)(v192 + 24) = v68;
        ++*(_QWORD *)v68;
        *(_DWORD *)(v192 + 36) = v191;
        *(_DWORD *)(v192 + 32) = -1;
        v193 = *(_QWORD *)(*(_QWORD *)(*(_QWORD *)(qword_143A35A28 + 504) + 16LL) + 744LL);
        v194 = *(_QWORD *)(v193 + 8);
        *(_QWORD *)&v195 = v193;
        v196 = v194 | *(_QWORD *)(v192 - 8) & 3LL;
        *(_QWORD *)v194 = v192 - 16;
        *((_QWORD *)&v195 + 1) = v196;
        *(_OWORD *)(v192 - 16) = v195;
        v80 = *(_QWORD *)v190 == 0;
        *(_QWORD *)(v193 + 8) = v192 - 16;
        *(_QWORD *)(v192 + 16) = v190;
        if ( v80 )
        {
          v386 = v192;
          (*(void (__fastcall **)(__int64))(*(_QWORD *)(v190 + 8) + 48LL))(a1: v190);
          v192 = v386;
        }
        v190 = v192;
      }
    }
    else
    {
      v190 = *(_QWORD *)qword_1435FA6C0;
      if ( *(_QWORD *)qword_1435FA6C0 != 0 )
      {
        *(_QWORD *)qword_1435FA6C0 = *(_QWORD *)v190;
        *(_QWORD *)v190 = 1;
        --*(_DWORD *)qword_1435FA6D0;
      }
      else
      {
        v388 = v191;
        v221 = MEMORY[0x13B00DD60](a1: qword_143A35A88);
        v191 = v388;
        v190 = v221;
      }
      *(_QWORD *)(v190 + 24) = v68;
      *(_QWORD *)(v190 + 16) = 0;
      ++*(_QWORD *)v68;
      v205 = *(_QWORD *)(qword_143A35A28 + 504);
      *(_DWORD *)(v190 + 36) = v191;
      *(_DWORD *)(v190 + 32) = -1;
      v206 = *(_QWORD *)(*(_QWORD *)(v205 + 16) + 744LL);
      v207 = *(_QWORD *)(v206 + 8);
      *(_QWORD *)&v208 = v206;
      v209 = v207 | *(_QWORD *)(v190 - 8) & 3LL;
      *(_QWORD *)v207 = v190 - 16;
      *((_QWORD *)&v208 + 1) = v209;
      *(_OWORD *)(v190 - 16) = v208;
      *(_QWORD *)(v206 + 8) = v190 - 16;
    }
    ((void (__fastcall *)(__int64, void *, __int64 *, __int64 *))unk_142F544C0)(
      a1: v68,
      a2: &unk_1435A0338,
      a3: v299,
      a4: a35);
    if ( qword_143944148 == v68 )
    {
      v80 = (*(_QWORD *)v68)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(__int64))(*(_QWORD *)(v68 + 8) + 48LL))(a1: v68);
      qword_143944148 = 0;
    }
    v197 = a1[7];
    v198 = *(_QWORD *)(v197 + 8);
    v199 = *(_QWORD *)(v198 + 40);
    v200 = *(_QWORD **)(v199 + 16);
    *(_QWORD *)(v197 + 8) = *(_QWORD *)(v198 + 48);
    *(_DWORD *)(v199 + 64) = -1;
    if ( v200 != nullptr )
    {
      *(_QWORD *)(v199 + 16) = 0;
      v80 = (*v200)-- == 1;
      if ( v80 )
        (*(void (**)(void))(v200[1] + 48LL))();
    }
    v80 = (*(_QWORD *)v199)-- == 1;
    if ( v80 )
      (*(void (__fastcall **)(__int64))(*(_QWORD *)(v199 + 8) + 48LL))(a1: v199);
    *(_QWORD *)(v199 + 120) = 0;
    v201 = a35;
    if ( a35 != nullptr )
    {
      v331 = *a35;
      *v201 = v331 - 1;
      if ( v331 == 1 )
        (*(void (__fastcall **)(__int64 *))(v201[1] + 48))(a1: v201);
    }
    if ( v66 != nullptr )
    {
      v80 = (*v66)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(_QWORD *))(v66[1] + 48LL))(a1: v66);
    }
    if ( v75 != nullptr )
    {
      v80 = (*v75)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(_QWORD *))(v75[1] + 48LL))(a1: v75);
    }
    if ( v64 != nullptr )
    {
      v80 = (*v64)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(_QWORD *))(v64[1] + 48LL))(a1: v64);
    }
    if ( v67 != nullptr )
    {
      v80 = (*v67)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(_QWORD *))(v67[1] + 48LL))(a1: v67);
    }
    if ( v65 != nullptr )
    {
      v80 = (*v65)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(_QWORD *))(v65[1] + 48LL))(a1: v65);
    }
    if ( a36 != nullptr )
    {
      v80 = (*a36)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(_QWORD *))(a36[1] + 48LL))(a1: a36);
    }
    if ( v333 != nullptr )
    {
      v80 = (*v333)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(_QWORD *))(v333[1] + 48LL))(a1: v333);
    }
    if ( v335 != nullptr )
    {
      v80 = (*v335)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(_QWORD *))(v335[1] + 48LL))(a1: v335);
    }
    if ( v337 != nullptr )
    {
      v80 = (*v337)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(_QWORD *))(v337[1] + 48LL))(a1: v337);
    }
    if ( v339 != nullptr )
    {
      v80 = (*v339)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(_QWORD *))(v339[1] + 48LL))(a1: v339);
    }
    if ( v341 != nullptr )
    {
      v80 = (*v341)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(_QWORD *))(v341[1] + 48LL))(a1: v341);
    }
    if ( v346 != nullptr )
    {
      v80 = (*v346)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(_QWORD *))(v346[1] + 48LL))(a1: v346);
    }
    if ( v343 != nullptr )
    {
      v80 = (*v343)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(_QWORD *))(v343[1] + 48LL))(a1: v343);
    }
    if ( v347 != nullptr )
    {
      v80 = (*v347)-- == 1;
      if ( v80 )
        (*(void (**)(void))(v347[1] + 48LL))();
    }
    if ( v364 != nullptr )
    {
      v80 = (*v364)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(_QWORD *))(v364[1] + 48LL))(a1: v364);
    }
    if ( v371 != nullptr )
    {
      v80 = (*v371)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(_QWORD *))(v371[1] + 48LL))(a1: v371);
    }
    if ( v374 != nullptr )
    {
      v80 = (*v374)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(_QWORD *))(v374[1] + 48LL))(a1: v374);
    }
    if ( v373 != nullptr )
    {
      v80 = (*v373)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(__int64 *))(v373[1] + 48))(a1: v373);
    }
    if ( v372 != nullptr )
    {
      v80 = (*v372)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(__int64 *))(v372[1] + 48))(a1: v372);
    }
    if ( v370 != nullptr )
    {
      v80 = (*v370)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(__int64 *))(v370[1] + 48))(a1: v370);
    }
    if ( v368 != nullptr )
    {
      v80 = (*v368)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(__int64 *))(v368[1] + 48))(a1: v368);
    }
    if ( v369 != nullptr )
    {
      v80 = (*v369)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(__int64 *))(v369[1] + 48))(a1: v369);
    }
    if ( v367 != nullptr )
    {
      v80 = (*v367)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(__int64 *))(v367[1] + 48))(a1: v367);
    }
    if ( v365 != nullptr )
    {
      v80 = (*v365)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(_QWORD *))(v365[1] + 48LL))(a1: v365);
    }
    if ( v366 != nullptr )
    {
      v80 = (*v366)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(__int64 *))(v366[1] + 48))(a1: v366);
    }
    if ( v363 != nullptr )
    {
      v80 = (*v363)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(__int64 *))(v363[1] + 48))(a1: v363);
    }
    if ( v362 != nullptr )
    {
      v80 = (*v362)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(_QWORD *))(v362[1] + 48LL))(a1: v362);
    }
    if ( v354 != nullptr )
    {
      v80 = (*v354)-- == 1;
      if ( v80 )
        (*(void (__fastcall **)(_QWORD *))(v354[1] + 48LL))(a1: v354);
    }
    v202 = v299;
    v203 = v299;
    v301 = *v299;
    *v203 = v301 - 1;
    if ( v301 == 1 )
      (*(void (**)(void))(v202[1] + 48))();
    MEMORY[0x13B00DF80](a1, a2: v378, a3: v381, a4: v190);
    return nullptr;
  }
  v84 = MEMORY[0x13B054620](a1, a2: v299, a3: qword_14393FD60);
  v64 = (_QWORD *)v84;
  if ( v84 == 0 )
  {
    v212 = (_QWORD *)a1[12];
    v190 = a1[14];
    v65 = nullptr;
    a1[14] = 0;
    v67 = nullptr;
    v75 = nullptr;
    v191 = 31;
    v378 = v212;
    v354 = nullptr;
    v381 = (_QWORD *)a1[13];
    v362 = nullptr;
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v346 = nullptr;
    v341 = nullptr;
    v339 = nullptr;
    v337 = nullptr;
    v335 = nullptr;
    v333 = nullptr;
    a36 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v85 = MEMORY[0x13B054620](a1, a2: v84, a3: qword_14393FD70);
  v80 = (*v64)-- == 1;
  v75 = (_QWORD *)v85;
  if ( v80 )
    (*(void (__fastcall **)(_QWORD *))(v64[1] + 48LL))(a1: v64);
  if ( v75 == nullptr )
  {
    v214 = (_QWORD *)a1[12];
    v190 = a1[14];
    v65 = nullptr;
    a1[14] = 0;
    v67 = nullptr;
    v64 = nullptr;
    v191 = 31;
    v378 = v214;
    v354 = nullptr;
    v381 = (_QWORD *)a1[13];
    v362 = nullptr;
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v346 = nullptr;
    v341 = nullptr;
    v339 = nullptr;
    v337 = nullptr;
    v335 = nullptr;
    v333 = nullptr;
    a36 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v86 = MEMORY[0x13B054620](a1, a2: v299, a3: qword_14393FD60);
  v67 = (_QWORD *)v86;
  if ( v86 == 0 )
  {
    v216 = (_QWORD *)a1[12];
    v190 = a1[14];
    v65 = nullptr;
    a1[14] = 0;
    v64 = nullptr;
    v191 = 32;
    v378 = v216;
    v354 = nullptr;
    v381 = (_QWORD *)a1[13];
    v362 = nullptr;
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v346 = nullptr;
    v341 = nullptr;
    v339 = nullptr;
    v337 = nullptr;
    v335 = nullptr;
    v333 = nullptr;
    a36 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v87 = MEMORY[0x13B054620](a1, a2: v86, a3: qword_14393FD78);
  v80 = (*v67)-- == 1;
  v64 = (_QWORD *)v87;
  if ( v80 )
    (*(void (__fastcall **)(_QWORD *))(v67[1] + 48LL))(a1: v67);
  if ( v64 == nullptr )
  {
    v219 = (_QWORD *)a1[12];
    v190 = a1[14];
    v65 = nullptr;
    a1[14] = 0;
    v67 = nullptr;
    v191 = 32;
    v378 = v219;
    v354 = nullptr;
    v381 = (_QWORD *)a1[13];
    v362 = nullptr;
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v346 = nullptr;
    v341 = nullptr;
    v339 = nullptr;
    v337 = nullptr;
    v335 = nullptr;
    v333 = nullptr;
    a36 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v88 = MEMORY[0x13B054620](a1, a2: v299, a3: qword_14393FD60);
  v65 = (_QWORD *)v88;
  if ( v88 == 0 )
  {
    v220 = (_QWORD *)a1[12];
    v190 = a1[14];
    v67 = nullptr;
    a1[14] = 0;
    v191 = 33;
    v378 = v220;
    v354 = nullptr;
    v381 = (_QWORD *)a1[13];
    v362 = nullptr;
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v346 = nullptr;
    v341 = nullptr;
    v339 = nullptr;
    v337 = nullptr;
    v335 = nullptr;
    v333 = nullptr;
    a36 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v89 = MEMORY[0x13B054620](a1, a2: v88, a3: qword_14393FD80);
  v80 = (*v65)-- == 1;
  v67 = (_QWORD *)v89;
  if ( v80 )
    (*(void (__fastcall **)(_QWORD *))(v65[1] + 48LL))(a1: v65);
  if ( v67 == nullptr )
  {
    v217 = (_QWORD *)a1[12];
    v190 = a1[14];
    v65 = nullptr;
    a1[14] = 0;
    v191 = 33;
    v378 = v217;
    v354 = nullptr;
    v381 = (_QWORD *)a1[13];
    v362 = nullptr;
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v346 = nullptr;
    v341 = nullptr;
    v339 = nullptr;
    v337 = nullptr;
    v335 = nullptr;
    v333 = nullptr;
    a36 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v90 = MEMORY[0x13B054620](a1, a2: v299, a3: qword_14393FD60);
  a36 = (_QWORD *)v90;
  if ( v90 == 0 )
  {
    v222 = (_QWORD *)a1[12];
    v190 = a1[14];
    v65 = nullptr;
    a1[14] = 0;
    v191 = 34;
    v378 = v222;
    v354 = nullptr;
    v381 = (_QWORD *)a1[13];
    v362 = nullptr;
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v346 = nullptr;
    v341 = nullptr;
    v339 = nullptr;
    v337 = nullptr;
    v335 = nullptr;
    v333 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v91 = MEMORY[0x13B054620](a1, a2: v90, a3: qword_14393FD88);
  v92 = a36;
  v65 = (_QWORD *)v91;
  v332 = *a36;
  *v92 = v332 - 1;
  if ( v332 == 1 )
    (*(void (__fastcall **)(_QWORD *))(v92[1] + 48LL))(a1: v92);
  if ( v65 == nullptr )
  {
    v223 = (_QWORD *)a1[12];
    v190 = a1[14];
    v354 = nullptr;
    a1[14] = 0;
    v191 = 34;
    v378 = v223;
    v362 = nullptr;
    v381 = (_QWORD *)a1[13];
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v346 = nullptr;
    v341 = nullptr;
    v339 = nullptr;
    v337 = nullptr;
    v335 = nullptr;
    v333 = nullptr;
    a36 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v93 = MEMORY[0x13B054620](a1, a2: v299, a3: qword_14393FD60);
  v333 = (_QWORD *)v93;
  if ( v93 == 0 )
  {
    v224 = (_QWORD *)a1[12];
    v190 = a1[14];
    v354 = nullptr;
    a1[14] = 0;
    v191 = 35;
    v378 = v224;
    v362 = nullptr;
    v381 = (_QWORD *)a1[13];
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v346 = nullptr;
    v341 = nullptr;
    v339 = nullptr;
    v337 = nullptr;
    v335 = nullptr;
    a36 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v94 = MEMORY[0x13B054620](a1, a2: v93, a3: qword_14393FD90);
  v95 = v333;
  a36 = (_QWORD *)v94;
  v334 = *v333;
  *v95 = v334 - 1;
  if ( v334 == 1 )
    (*(void (__fastcall **)(_QWORD *))(v95[1] + 48LL))(a1: v95);
  if ( a36 == nullptr )
  {
LABEL_414:
    v225 = (_QWORD *)a1[12];
    v190 = a1[14];
    v354 = nullptr;
    a1[14] = 0;
    v191 = 35;
    v378 = v225;
    v362 = nullptr;
    v381 = (_QWORD *)a1[13];
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v346 = nullptr;
    v341 = nullptr;
    v339 = nullptr;
    v337 = nullptr;
    v335 = nullptr;
    v333 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v96 = MEMORY[0x13B054620](a1, a2: v299, a3: qword_14393FD60);
  v335 = (_QWORD *)v96;
  if ( v96 == 0 )
  {
    v226 = (_QWORD *)a1[12];
    v190 = a1[14];
    v354 = nullptr;
    a1[14] = 0;
    v191 = 36;
    v378 = v226;
    v362 = nullptr;
    v381 = (_QWORD *)a1[13];
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v346 = nullptr;
    v341 = nullptr;
    v339 = nullptr;
    v337 = nullptr;
    v333 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v97 = MEMORY[0x13B054620](a1, a2: v96, a3: qword_14393FD98);
  v98 = v335;
  v333 = (_QWORD *)v97;
  v336 = *v335;
  *v98 = v336 - 1;
  if ( v336 == 1 )
    (*(void (__fastcall **)(_QWORD *))(v98[1] + 48LL))(a1: v98);
  if ( v333 == nullptr )
  {
    v227 = (_QWORD *)a1[12];
    v190 = a1[14];
    v354 = nullptr;
    a1[14] = 0;
    v191 = 36;
    v378 = v227;
    v362 = nullptr;
    v381 = (_QWORD *)a1[13];
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v346 = nullptr;
    v341 = nullptr;
    v339 = nullptr;
    v337 = nullptr;
    v335 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v99 = MEMORY[0x13B054620](a1, a2: v299, a3: qword_14393FD60);
  v337 = (_QWORD *)v99;
  if ( v99 == 0 )
  {
    v228 = (_QWORD *)a1[12];
    v190 = a1[14];
    v354 = nullptr;
    a1[14] = 0;
    v191 = 37;
    v378 = v228;
    v362 = nullptr;
    v381 = (_QWORD *)a1[13];
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v346 = nullptr;
    v341 = nullptr;
    v339 = nullptr;
    v335 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v100 = MEMORY[0x13B054620](a1, a2: v99, a3: qword_14393FDA0);
  v101 = v337;
  v335 = (_QWORD *)v100;
  v338 = *v337;
  *v101 = v338 - 1;
  if ( v338 == 1 )
    (*(void (__fastcall **)(_QWORD *))(v101[1] + 48LL))(a1: v101);
  if ( v335 == nullptr )
  {
    v218 = (_QWORD *)a1[12];
    v190 = a1[14];
    v354 = nullptr;
    a1[14] = 0;
    v191 = 37;
    v378 = v218;
    v362 = nullptr;
    v381 = (_QWORD *)a1[13];
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v346 = nullptr;
    v341 = nullptr;
    v339 = nullptr;
    v337 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v102 = MEMORY[0x13B054620](a1, a2: v299, a3: qword_14393FD60);
  v339 = (_QWORD *)v102;
  if ( v102 == 0 )
  {
    v229 = (_QWORD *)a1[12];
    v190 = a1[14];
    v354 = nullptr;
    a1[14] = 0;
    v191 = 38;
    v378 = v229;
    v362 = nullptr;
    v381 = (_QWORD *)a1[13];
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v346 = nullptr;
    v341 = nullptr;
    v337 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v103 = MEMORY[0x13B054620](a1, a2: v102, a3: qword_14393FDA8);
  v104 = v339;
  v337 = (_QWORD *)v103;
  v340 = *v339;
  *v104 = v340 - 1;
  if ( v340 == 1 )
    (*(void (__fastcall **)(_QWORD *))(v104[1] + 48LL))(a1: v104);
  if ( v337 == nullptr )
  {
    v230 = (_QWORD *)a1[12];
    v190 = a1[14];
    v354 = nullptr;
    a1[14] = 0;
    v191 = 38;
    v378 = v230;
    v362 = nullptr;
    v381 = (_QWORD *)a1[13];
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v346 = nullptr;
    v341 = nullptr;
    v339 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v105 = MEMORY[0x13B054620](a1, a2: v299, a3: qword_14393FD60);
  v341 = (_QWORD *)v105;
  if ( v105 == 0 )
  {
    v231 = (_QWORD *)a1[12];
    v190 = a1[14];
    v354 = nullptr;
    a1[14] = 0;
    v191 = 39;
    v378 = v231;
    v362 = nullptr;
    v381 = (_QWORD *)a1[13];
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v346 = nullptr;
    v339 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v106 = MEMORY[0x13B054620](a1, a2: v105, a3: qword_14393FDB0);
  v107 = v341;
  v339 = (_QWORD *)v106;
  v342 = *v341;
  *v107 = v342 - 1;
  if ( v342 == 1 )
    (*(void (__fastcall **)(_QWORD *))(v107[1] + 48LL))(a1: v107);
  if ( v339 == nullptr )
  {
    v232 = (_QWORD *)a1[12];
    v190 = a1[14];
    v354 = nullptr;
    a1[14] = 0;
    v191 = 39;
    v378 = v232;
    v362 = nullptr;
    v381 = (_QWORD *)a1[13];
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v346 = nullptr;
    v341 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v108 = MEMORY[0x13B054620](a1, a2: v299, a3: qword_14393FD60);
  v346 = (_QWORD *)v108;
  if ( v108 == 0 )
  {
    v233 = (_QWORD *)a1[12];
    v190 = a1[14];
    v354 = nullptr;
    a1[14] = 0;
    v191 = 41;
    v378 = v233;
    v362 = nullptr;
    v381 = (_QWORD *)a1[13];
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v341 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v341 = (_QWORD *)MEMORY[0x13B054620](a1, a2: v108, a3: qword_14393FDB8);
  v80 = (*v346)-- == 1;
  if ( v80 )
    (*(void (__fastcall **)(_QWORD *))(v346[1] + 48LL))(a1: v346);
  if ( v341 == nullptr )
  {
    v235 = (_QWORD *)a1[12];
    v190 = a1[14];
    v354 = nullptr;
    a1[14] = 0;
    v191 = 41;
    v378 = v235;
    v362 = nullptr;
    v381 = (_QWORD *)a1[13];
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    v346 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v109 = MEMORY[0x13B054620](a1, a2: v299, a3: qword_14393FD60);
  v343 = (_QWORD *)v109;
  if ( v109 == 0 )
  {
    v236 = (_QWORD *)a1[12];
    v190 = a1[14];
    v354 = nullptr;
    a1[14] = 0;
    v191 = 42;
    v378 = v236;
    v362 = nullptr;
    v381 = (_QWORD *)a1[13];
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v346 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v110 = MEMORY[0x13B054620](a1, a2: v109, a3: qword_14393FDC0);
  v111 = v343;
  v346 = (_QWORD *)v110;
  v344 = *v343;
  *v111 = v344 - 1;
  if ( v344 == 1 )
    (*(void (__fastcall **)(_QWORD *))(v111[1] + 48LL))(a1: v111);
  if ( v346 == nullptr )
  {
    v237 = (_QWORD *)a1[12];
    v190 = a1[14];
    v354 = nullptr;
    a1[14] = 0;
    v191 = 42;
    v378 = v237;
    v362 = nullptr;
    v381 = (_QWORD *)a1[13];
    v363 = nullptr;
    v366 = nullptr;
    v365 = nullptr;
    v367 = nullptr;
    v369 = nullptr;
    v368 = nullptr;
    v370 = nullptr;
    v372 = nullptr;
    v373 = nullptr;
    v374 = nullptr;
    v371 = nullptr;
    v364 = nullptr;
    v347 = nullptr;
    v343 = nullptr;
    *((_OWORD *)a1 + 6) = 0;
    goto LABEL_281;
  }
  v112 = MEMORY[0x13B054620](a1, a2: v299, a3: qword_14393FD60);
  v343 = (_QWORD *)v112;
  if ( v112 != 0 )
  {
    v113 = MEMORY[0x13B054620](a1, a2: v112, a3: qword_14393FDC8);
    v114 = v343;
    v347 = (_QWORD *)v113;
    v345 = *v343;
    *v114 = v345 - 1;
    if ( v345 == 1 )
      (*(void (__fastcall **)(_QWORD *))(v114[1] + 48LL))(a1: v114);
    if ( v347 == nullptr )
    {
      v239 = (_QWORD *)a1[12];
      v190 = a1[14];
      v354 = nullptr;
      a1[14] = 0;
      v191 = 44;
      v378 = v239;
      v362 = nullptr;
      v381 = (_QWORD *)a1[13];
      v363 = nullptr;
      v366 = nullptr;
      v365 = nullptr;
      v367 = nullptr;
      v369 = nullptr;
      v368 = nullptr;
      v370 = nullptr;
      v372 = nullptr;
      v373 = nullptr;
      v374 = nullptr;
      v371 = nullptr;
      v364 = nullptr;
      v343 = nullptr;
      *((_OWORD *)a1 + 6) = 0;
      goto LABEL_281;
    }
    v115 = MEMORY[0x13B054620](a1, a2: v347, a3: qword_14393FDD0);
    v116 = v347;
    v343 = (_QWORD *)v115;
    v348 = *v347;
    *v116 = v348 - 1;
    if ( v348 == 1 )
      (*(void (__fastcall **)(_QWORD *))(v116[1] + 48LL))(a1: v116);
    if ( v343 != nullptr )
    {
      v117 = MEMORY[0x13B054620](a1, a2: v299, a3: qword_14393FD60);
      v347 = (_QWORD *)v117;
      if ( v117 != 0 )
      {
        v118 = MEMORY[0x13B054620](a1, a2: v117, a3: qword_14393FDC8);
        v119 = v347;
        v364 = (_QWORD *)v118;
        v349 = *v347;
        *v119 = v349 - 1;
        if ( v349 == 1 )
          (*(void (__fastcall **)(_QWORD *))(v119[1] + 48LL))(a1: v119);
        if ( v364 == nullptr )
        {
          v190 = a1[14];
          v191 = 45;
          v378 = (_QWORD *)a1[12];
          v241 = (_QWORD *)a1[13];
          *((_OWORD *)a1 + 6) = 0;
          v381 = v241;
          a1[14] = 0;
          v354 = nullptr;
          v362 = nullptr;
          v363 = nullptr;
          v366 = nullptr;
          v365 = nullptr;
          v367 = nullptr;
          v369 = nullptr;
          v368 = nullptr;
          v370 = nullptr;
          v372 = nullptr;
          v373 = nullptr;
          v374 = nullptr;
          v371 = nullptr;
          v347 = nullptr;
          goto LABEL_281;
        }
        v347 = (_QWORD *)MEMORY[0x13B054620](a1, a2: v364, a3: qword_14393FDD8);
        v80 = (*v364)-- == 1;
        if ( v80 )
          (*(void (__fastcall **)(_QWORD *))(v364[1] + 48LL))(a1: v364);
        if ( v347 != nullptr )
        {
          v120 = MEMORY[0x13B054620](a1, a2: v299, a3: qword_14393FD60);
          v364 = (_QWORD *)v120;
          if ( v120 != 0 )
          {
            v371 = (_QWORD *)MEMORY[0x13B054620](a1, a2: v120, a3: qword_14393FDC8);
            v80 = (*v364)-- == 1;
            if ( v80 )
              (*(void (__fastcall **)(_QWORD *))(v364[1] + 48LL))(a1: v364);
            if ( v371 == nullptr )
            {
              v190 = a1[14];
              v191 = 46;
              v378 = (_QWORD *)a1[12];
              v243 = (_QWORD *)a1[13];
              *((_OWORD *)a1 + 6) = 0;
              v381 = v243;
              a1[14] = 0;
              v354 = nullptr;
              v362 = nullptr;
              v363 = nullptr;
              v366 = nullptr;
              v365 = nullptr;
              v367 = nullptr;
              v369 = nullptr;
              v368 = nullptr;
              v370 = nullptr;
              v372 = nullptr;
              v373 = nullptr;
              v374 = nullptr;
              v364 = nullptr;
              goto LABEL_281;
            }
            v364 = (_QWORD *)MEMORY[0x13B054620](a1, a2: v371, a3: qword_14393FDE0);
            v80 = (*v371)-- == 1;
            if ( v80 )
              (*(void (__fastcall **)(_QWORD *))(v371[1] + 48LL))(a1: v371);
            if ( v364 != nullptr )
            {
              v121 = MEMORY[0x13B054620](a1, a2: v299, a3: qword_14393FD60);
              v371 = (_QWORD *)v121;
              if ( v121 != 0 )
              {
                v374 = (_QWORD *)MEMORY[0x13B054620](a1, a2: v121, a3: qword_14393FDC8);
                v80 = (*v371)-- == 1;
                if ( v80 )
                  (*(void (__fastcall **)(_QWORD *))(v371[1] + 48LL))(a1: v371);
                if ( v374 == nullptr )
                {
                  v190 = a1[14];
                  v191 = 47;
                  v378 = (_QWORD *)a1[12];
                  v245 = (_QWORD *)a1[13];
                  *((_OWORD *)a1 + 6) = 0;
                  v381 = v245;
                  a1[14] = 0;
                  v354 = nullptr;
                  v362 = nullptr;
                  v363 = nullptr;
                  v366 = nullptr;
                  v365 = nullptr;
                  v367 = nullptr;
                  v369 = nullptr;
                  v368 = nullptr;
                  v370 = nullptr;
                  v372 = nullptr;
                  v373 = nullptr;
                  v371 = nullptr;
                  goto LABEL_281;
                }
                v371 = (_QWORD *)MEMORY[0x13B054620](a1, a2: v374, a3: qword_14393FDE8);
                v80 = (*v374)-- == 1;
                if ( v80 )
                  MEMORY[0x13B0039F0](a1: v374);
                if ( v371 != nullptr )
                {
                  v122 = MEMORY[0x13B054620](a1, a2: v299, a3: qword_14393FD60);
                  v374 = (_QWORD *)v122;
                  if ( v122 != 0 )
                  {
                    v373 = (__int64 *)MEMORY[0x13B054620](a1, a2: v122, a3: qword_14393FDC8);
                    v80 = (*v374)-- == 1;
                    if ( v80 )
                      MEMORY[0x13B0039F0](a1: v374);
                    if ( v373 == nullptr )
                    {
                      v190 = a1[14];
                      v191 = 49;
                      v378 = (_QWORD *)a1[12];
                      v247 = (_QWORD *)a1[13];
                      *((_OWORD *)a1 + 6) = 0;
                      v381 = v247;
                      a1[14] = 0;
                      v354 = nullptr;
                      v362 = nullptr;
                      v363 = nullptr;
                      v366 = nullptr;
                      v365 = nullptr;
                      v367 = nullptr;
                      v369 = nullptr;
                      v368 = nullptr;
                      v370 = nullptr;
                      v372 = nullptr;
                      v374 = nullptr;
                      goto LABEL_281;
                    }
                    v374 = (_QWORD *)MEMORY[0x13B054620](a1, a2: v373, a3: qword_14393FDF0);
                    v80 = (*v373)-- == 1;
                    if ( v80 )
                      MEMORY[0x13B0039F0](a1: v373);
                    if ( v374 != nullptr )
                    {
                      v373 = (__int64 *)MEMORY[0x13B054620](a1, a2: v299, a3: qword_14393FD60);
                      if ( v373 != nullptr )
                      {
                        v372 = (__int64 *)MEMORY[0x13B054620](a1, a2: v373, a3: qword_14393FDC8);
                        v80 = (*v373)-- == 1;
                        if ( v80 )
                          MEMORY[0x13B0039F0](a1: v373);
                        if ( v372 == nullptr )
                        {
                          v190 = a1[14];
                          v354 = nullptr;
                          v191 = 50;
                          v378 = (_QWORD *)a1[12];
                          v249 = (_QWORD *)a1[13];
                          a1[14] = 0;
                          v381 = v249;
                          v362 = nullptr;
                          v363 = nullptr;
                          v366 = nullptr;
                          v365 = nullptr;
                          v367 = nullptr;
                          v369 = nullptr;
                          v368 = nullptr;
                          v370 = nullptr;
                          v373 = nullptr;
                          *((_OWORD *)a1 + 6) = 0;
                          goto LABEL_281;
                        }
                        v373 = (__int64 *)MEMORY[0x13B054620](a1, a2: v372, a3: qword_14393FDF8);
                        v80 = (*v372)-- == 1;
                        if ( v80 )
                          MEMORY[0x13B0039F0](a1: v372);
                        if ( v373 != nullptr )
                        {
                          v372 = (__int64 *)MEMORY[0x13B054620](a1, a2: v299, a3: qword_14393FD60);
                          if ( v372 != nullptr )
                          {
                            v370 = (__int64 *)MEMORY[0x13B054620](a1, a2: v372, a3: qword_14393FDC8);
                            v80 = (*v372)-- == 1;
                            if ( v80 )
                              MEMORY[0x13B0039F0](a1: v372);
                            if ( v370 == nullptr )
                            {
                              v190 = a1[14];
                              v354 = nullptr;
                              v191 = 51;
                              v378 = (_QWORD *)a1[12];
                              v251 = (_QWORD *)a1[13];
                              a1[14] = 0;
                              v381 = v251;
                              v362 = nullptr;
                              v363 = nullptr;
                              v366 = nullptr;
                              v365 = nullptr;
                              v367 = nullptr;
                              v369 = nullptr;
                              v368 = nullptr;
                              v372 = nullptr;
                              *((_OWORD *)a1 + 6) = 0;
                              goto LABEL_281;
                            }
                            v372 = (__int64 *)MEMORY[0x13B054620](a1, a2: v370, a3: qword_14393FE00);
                            v80 = (*v370)-- == 1;
                            if ( v80 )
                              MEMORY[0x13B0039F0](a1: v370);
                            if ( v372 != nullptr )
                            {
                              v370 = (__int64 *)MEMORY[0x13B054620](a1, a2: v299, a3: qword_14393FD60);
                              if ( v370 != nullptr )
                              {
                                v368 = (__int64 *)MEMORY[0x13B054620](a1, a2: v370, a3: qword_14393FDC8);
                                v80 = (*v370)-- == 1;
                                if ( v80 )
                                  MEMORY[0x13B0039F0](a1: v370);
                                if ( v368 == nullptr )
                                {
                                  v190 = a1[14];
                                  v354 = nullptr;
                                  v378 = (_QWORD *)a1[12];
                                  v253 = (_QWORD *)a1[13];
                                  a1[14] = 0;
                                  v362 = nullptr;
                                  v363 = nullptr;
                                  v366 = nullptr;
                                  v365 = nullptr;
                                  v367 = nullptr;
                                  v369 = nullptr;
                                  v370 = nullptr;
                                  v191 = 52;
                                  v381 = v253;
                                  *((_OWORD *)a1 + 6) = 0;
                                  goto LABEL_281;
                                }
                                v370 = (__int64 *)MEMORY[0x13B054620](a1, a2: v368, a3: qword_14393FE08);
                                v80 = (*v368)-- == 1;
                                if ( v80 )
                                  MEMORY[0x13B0039F0](a1: v368);
                                if ( v370 != nullptr )
                                {
                                  v368 = (__int64 *)MEMORY[0x13B054620](a1, a2: v299, a3: qword_14393FD60);
                                  if ( v368 != nullptr )
                                  {
                                    v369 = (__int64 *)MEMORY[0x13B054620](a1, a2: v368, a3: qword_14393FDC8);
                                    v80 = (*v368)-- == 1;
                                    if ( v80 )
                                      MEMORY[0x13B0039F0](a1: v368);
                                    if ( v369 == nullptr )
                                    {
                                      v190 = a1[14];
                                      v191 = 53;
                                      v378 = (_QWORD *)a1[12];
                                      v262 = (_QWORD *)a1[13];
                                      *((_OWORD *)a1 + 6) = 0;
                                      v381 = v262;
                                      a1[14] = 0;
                                      v354 = nullptr;
                                      v362 = nullptr;
                                      v363 = nullptr;
                                      v366 = nullptr;
                                      v365 = nullptr;
                                      v367 = nullptr;
                                      v368 = nullptr;
                                      goto LABEL_281;
                                    }
                                    v368 = (__int64 *)MEMORY[0x13B054620](a1, a2: v369, a3: qword_14393FE10);
                                    v80 = (*v369)-- == 1;
                                    if ( v80 )
                                      MEMORY[0x13B0039F0](a1: v369);
                                    if ( v368 != nullptr )
                                    {
                                      v367 = (__int64 *)MEMORY[0x13B054620](a1, a2: v299, a3: qword_14393FD60);
                                      if ( v367 == nullptr )
                                      {
                                        v190 = a1[14];
                                        v191 = 54;
                                        v378 = (_QWORD *)a1[12];
                                        v261 = (_QWORD *)a1[13];
                                        *((_OWORD *)a1 + 6) = 0;
                                        v381 = v261;
                                        a1[14] = 0;
                                        v354 = nullptr;
                                        v362 = nullptr;
                                        v363 = nullptr;
                                        v366 = nullptr;
                                        v365 = nullptr;
                                        v369 = nullptr;
                                        goto LABEL_281;
                                      }
                                      v369 = (__int64 *)MEMORY[0x13B054620](a1, a2: v367, a3: qword_14393FE18);
                                      v80 = (*v367)-- == 1;
                                      if ( v80 )
                                        MEMORY[0x13B0039F0](a1: v367);
                                      if ( v369 == nullptr )
                                      {
                                        v190 = a1[14];
                                        v191 = 54;
                                        v378 = (_QWORD *)a1[12];
                                        v273 = (_QWORD *)a1[13];
                                        *((_OWORD *)a1 + 6) = 0;
                                        v381 = v273;
                                        a1[14] = 0;
                                        v354 = nullptr;
                                        v362 = nullptr;
                                        v363 = nullptr;
                                        v366 = nullptr;
                                        v365 = nullptr;
                                        v367 = nullptr;
                                        goto LABEL_281;
                                      }
                                      v367 = (__int64 *)((__int64 (*)(void))unk_14321A720)();
                                      if ( v367 == nullptr )
                                      {
                                        ((void (__fastcall *)(_QWORD *, _QWORD **, __int64))unk_142F6E530)(
                                          a1,
                                          a2: &a62,
                                          a3: qword_14393FE20);
                                        v190 = a64;
                                        v354 = nullptr;
                                        v191 = 56;
                                        v378 = a62;
                                        v362 = nullptr;
                                        v381 = a63;
                                        v363 = nullptr;
                                        v366 = nullptr;
                                        v365 = nullptr;
                                        goto LABEL_281;
                                      }
                                      v123 = ((__int64 (__fastcall *)(_QWORD *, __int64 *))unk_1432AA300)(
                                               a1: v75,
                                               a2: v367);
                                      if ( v123 == -1 )
                                        goto LABEL_473;
                                      if ( v123 != 1 )
                                      {
LABEL_141:
                                        v367 = (__int64 *)qword_143A35200;
                                        goto LABEL_142;
                                      }
                                      v263 = *(_QWORD *)(*(_QWORD *)&qword_14393FD08[0] + 32LL);
                                      if ( *(_BYTE *)(v263 + 10) != 0 )
                                      {
                                        v264 = *(_DWORD *)(v263 + 12);
                                        if ( v264 == 0 )
                                        {
                                          v264 = dword_143547A4C;
                                          *(_DWORD *)(v263 + 12) = dword_143547A4C++;
                                        }
                                        if ( dword_143547A44 != v264 )
                                        {
                                          v357 = v263;
                                          dword_143547A44 = v264;
                                          v265 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
                                                   a1: v263,
                                                   a2: qword_14393FE28,
                                                   a3: *(_QWORD *)(qword_14393FE28 + 24));
                                          v263 = v357;
                                          qword_143944130 = v265;
                                        }
                                        if ( qword_143944130 >= 0 )
                                        {
                                          if ( *(_QWORD *)(v263
                                                         + (1LL << *(_BYTE *)(v263 + 9))
                                                         + 32
                                                         + 16 * qword_143944130
                                                         + 8) != 0 )
                                            goto LABEL_463;
                                          v358 = v263 + (1LL << *(_BYTE *)(v263 + 9)) + 32;
                                          v272 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
                                                   a1: v263,
                                                   a2: qword_14393FE28,
                                                   a3: *(_QWORD *)(qword_14393FE28 + 24));
                                          qword_143944130 = v272;
                                          if ( v272 >= 0 )
                                          {
                                            v268 = *(_QWORD *)(v358 + 16 * v272 + 8);
LABEL_468:
                                            if ( v268 != 0 )
                                              goto LABEL_463;
                                          }
                                        }
                                      }
                                      else
                                      {
                                        v267 = (__int64 *)MEMORY[0x13B02A410](
                                                            a1: *(_QWORD *)&qword_14393FD08[0],
                                                            a2: qword_14393FE28);
                                        if ( v267 != nullptr )
                                        {
                                          v268 = *v267;
                                          goto LABEL_468;
                                        }
                                      }
                                      v269 = (_QWORD *)MEMORY[0x13B02A410](
                                                         a1: *(_QWORD *)qword_1435FA560,
                                                         a2: qword_14393FE28);
                                      if ( v269 == nullptr || *v269 == 0 )
                                      {
                                        ((void (__fastcall *)(_QWORD *, _QWORD **, __int64))unk_142F6E530)(
                                          a1,
                                          a2: &a62,
                                          a3: qword_14393FE28);
                                        v190 = a64;
                                        v378 = a62;
                                        v381 = a63;
LABEL_472:
                                        v191 = 56;
                                        v354 = nullptr;
                                        v362 = nullptr;
                                        v363 = nullptr;
                                        v366 = nullptr;
                                        v365 = nullptr;
                                        v367 = nullptr;
                                        goto LABEL_281;
                                      }
LABEL_463:
                                      v266 = ((__int64 (__fastcall *)(_QWORD *))unk_1432AA300)(a1: v64);
                                      if ( v266 == -1 )
                                      {
LABEL_473:
                                        v270 = (_QWORD *)a1[12];
                                        v190 = a1[14];
                                        a1[14] = 0;
                                        v378 = v270;
                                        v271 = (_QWORD *)a1[13];
                                        *((_OWORD *)a1 + 6) = 0;
                                        v381 = v271;
                                        goto LABEL_472;
                                      }
                                      if ( v266 != 1 )
                                        goto LABEL_141;
                                      v367 = (__int64 *)qword_143A35208;
LABEL_142:
                                      ++*v367;
                                      v124 = ((__int64 (*)(void))unk_14321A480)();
                                      v365 = (_QWORD *)v124;
                                      if ( v124 == 0 )
                                      {
                                        ((void (__fastcall *)(_QWORD *, _QWORD **, __int64))unk_142F6E530)(
                                          a1,
                                          a2: &a62,
                                          a3: qword_14393FE30);
                                        v190 = a64;
                                        v354 = nullptr;
                                        v191 = 58;
                                        v378 = a62;
                                        v362 = nullptr;
                                        v381 = a63;
                                        v363 = nullptr;
                                        v366 = nullptr;
                                        goto LABEL_281;
                                      }
                                      *(_DWORD *)(v68 + 40) = 58;
                                      a62 = v66;
                                      STACK[0x510] = (unsigned __int64)a36;
                                      a63 = v75;
                                      STACK[0x518] = (unsigned __int64)v333;
                                      a64 = (__int64)v64;
                                      STACK[0x520] = (unsigned __int64)v335;
                                      STACK[0x500] = (unsigned __int64)v67;
                                      STACK[0x528] = (unsigned __int64)v339;
                                      STACK[0x508] = (unsigned __int64)v65;
                                      STACK[0x530] = (unsigned __int64)v337;
                                      STACK[0x538] = (unsigned __int64)v343;
                                      STACK[0x540] = (unsigned __int64)v347;
                                      STACK[0x548] = (unsigned __int64)v364;
                                      STACK[0x550] = (unsigned __int64)v341;
                                      STACK[0x558] = (unsigned __int64)v346;
                                      STACK[0x560] = (unsigned __int64)v371;
                                      STACK[0x568] = (unsigned __int64)v374;
                                      STACK[0x570] = (unsigned __int64)v373;
                                      v125 = *(_QWORD **)(v124 + 8);
                                      STACK[0x578] = (unsigned __int64)v372;
                                      STACK[0x598] = (unsigned __int64)v367;
                                      STACK[0x580] = (unsigned __int64)v369;
                                      STACK[0x588] = (unsigned __int64)v370;
                                      STACK[0x590] = (unsigned __int64)v368;
                                      v126 = v124;
                                      v127 = (__int64 (__fastcall *)(__int64, __int64))v125[18];
                                      if ( v127 != nullptr )
                                      {
                                        v350 = v125;
                                        v128 = v127(a1: v126, a2: qword_14393FE38);
                                        v129 = (_QWORD *)v128;
                                        if ( v128 == 0 )
                                        {
LABEL_512:
                                          v190 = a1[14];
                                          v354 = nullptr;
                                          v191 = 58;
                                          v378 = (_QWORD *)a1[12];
                                          v362 = nullptr;
                                          v381 = (_QWORD *)a1[13];
                                          a1[14] = 0;
                                          v363 = nullptr;
                                          v366 = nullptr;
                                          v365 = nullptr;
                                          *((_OWORD *)a1 + 6) = 0;
                                          goto LABEL_281;
                                        }
                                        v130 = *(_QWORD *)(v128 + 8);
                                        v131 = *(__int64 (__fastcall **)(_QWORD *, _QWORD *, _QWORD *))(v130 + 272);
                                        if ( v131 != nullptr && *(_QWORD *)(v130 + 280) != 0 )
                                        {
                                          v132 = v350;
                                          v351 = v129;
                                          v133 = v131(a1: v129, a2: v365, a3: v132);
                                          v134 = v351;
                                          v135 = (_QWORD *)v133;
                                          v80 = (*v351)-- == 1;
                                          if ( v80 )
                                          {
                                            v352 = v133;
                                            (*(void (__fastcall **)(_QWORD *, __int64))(v134[1] + 48LL))(
                                              a1: v134,
                                              a2: v133);
                                            v135 = (_QWORD *)v352;
                                          }
                                          if ( v135 == nullptr )
                                            goto LABEL_512;
                                          v353 = v135;
                                          v365 = (_QWORD *)MEMORY[0x13B00CC80](a1, a2: v135, a3: &a62);
                                          v80 = (*v353)-- == 1;
                                          if ( v80 )
                                            (*(void (__fastcall **)(_QWORD *))(v353[1] + 48LL))(a1: v353);
                                          goto LABEL_152;
                                        }
                                        v361 = v129;
                                        v365 = (_QWORD *)MEMORY[0x13B00CC80](a1, a2: v129, a3: &a62);
                                        v80 = (*v361)-- == 1;
                                        if ( !v80 )
                                          goto LABEL_152;
LABEL_510:
                                        MEMORY[0x13B0039F0](a1: v361);
                                        goto LABEL_152;
                                      }
                                      v296 = (__int64 (__fastcall *)(_QWORD *, __int64))v125[8];
                                      if ( v296 == nullptr )
                                      {
                                        qword_143A358D8(a1: *(_QWORD *)qword_143A353A8, a2: &unk_1435A0310, a3: v125[3]);
                                        goto LABEL_512;
                                      }
                                      if ( (*(_BYTE *)(qword_14393FE38 + 32) & 0x40) != 0
                                        && (*(_BYTE *)(qword_14393FE38 + 32) & 0x20) != 0 )
                                      {
                                        v297 = qword_14393FE38 + 48;
                                      }
                                      else
                                      {
                                        v297 = *(_QWORD *)(qword_14393FE38 + 56);
                                      }
                                      v298 = v296(a1: v365, a2: v297);
                                      if ( v298 == 0 )
                                        goto LABEL_512;
                                      v361 = (_QWORD *)v298;
                                      v365 = (_QWORD *)MEMORY[0x13B00CC80](a1, a2: v298, a3: &a62);
                                      v80 = (*v361)-- == 1;
                                      if ( v80 )
                                        goto LABEL_510;
LABEL_152:
                                      if ( v365 == nullptr )
                                        goto LABEL_512;
                                      *(_DWORD *)(v68 + 40) = 66;
                                      v363 = (__int64 *)((__int64 (__fastcall *)(_QWORD *, __int64, _QWORD, __int64))unk_142F86D60)(
                                                          a1,
                                                          a2: qword_14393FE40,
                                                          a3: *(_QWORD *)&qword_14393FD08[0],
                                                          a4: qword_143A35618);
                                      if ( v363 == nullptr )
                                      {
                                        v190 = a1[14];
                                        v191 = 66;
                                        v378 = (_QWORD *)a1[12];
                                        v295 = (_QWORD *)a1[13];
                                        *((_OWORD *)a1 + 6) = 0;
                                        v381 = v295;
                                        a1[14] = 0;
                                        v354 = nullptr;
                                        v362 = nullptr;
                                        v366 = nullptr;
                                        goto LABEL_281;
                                      }
                                      v136 = v363[1];
                                      if ( v136 == qword_143A355C8
                                        || (unsigned int)qword_143A35780(a1: v136, a2: qword_143A355C8) != 0 )
                                      {
                                        v366 = (__int64 *)((__int64 (__fastcall *)(_QWORD *, __int64 *, _QWORD, __int64))unk_142F524B0)(
                                                            a1,
                                                            a2: v363,
                                                            a3: *(_QWORD *)&qword_14393FD08[0],
                                                            a4: qword_14393FE50);
                                      }
                                      else
                                      {
                                        v366 = (__int64 *)((__int64 (__fastcall *)(_QWORD *, __int64 *, __int64))unk_142F52460)(
                                                            a1,
                                                            a2: v363,
                                                            a3: qword_14393FE50);
                                      }
                                      v80 = (*v363)-- == 1;
                                      if ( v80 )
                                        MEMORY[0x13B0039F0](a1: v363);
                                      if ( v366 == nullptr )
                                      {
                                        v190 = a1[14];
                                        v191 = 66;
                                        v378 = (_QWORD *)a1[12];
                                        v294 = (_QWORD *)a1[13];
                                        *((_OWORD *)a1 + 6) = 0;
                                        v381 = v294;
                                        a1[14] = 0;
                                        v354 = nullptr;
                                        v362 = nullptr;
                                        v363 = nullptr;
                                        goto LABEL_281;
                                      }
                                      v354 = (_QWORD *)((__int64 (__fastcall *)(__int64 *, __int64))unk_1430EC890)(
                                                         a1: v366,
                                                         a2: qword_14393FE58);
                                      if ( v354 == nullptr )
                                      {
                                        v190 = a1[14];
                                        v191 = 67;
                                        v378 = (_QWORD *)a1[12];
                                        v293 = (_QWORD *)a1[13];
                                        *((_OWORD *)a1 + 6) = 0;
                                        v381 = v293;
                                        a1[14] = 0;
                                        v362 = nullptr;
                                        v363 = nullptr;
                                        goto LABEL_281;
                                      }
                                      v362 = (_QWORD *)MEMORY[0x13B054620](a1, a2: v299, a3: qword_14393FD60);
                                      if ( v362 == nullptr )
                                      {
                                        v291 = v354;
                                        v190 = a1[14];
                                        v378 = (_QWORD *)a1[12];
                                        v292 = (_QWORD *)a1[13];
                                        *((_OWORD *)a1 + 6) = 0;
                                        v381 = v292;
                                        a1[14] = 0;
                                        v360 = *v354;
                                        *v291 = v360 - 1;
                                        if ( v360 == 1 )
                                        {
                                          MEMORY[0x13B0039F0](a1: v291);
                                          v191 = 67;
                                          v354 = nullptr;
                                          v363 = nullptr;
                                        }
                                        else
                                        {
                                          v354 = nullptr;
                                          v363 = nullptr;
                                          v191 = 67;
                                        }
                                        goto LABEL_281;
                                      }
                                      v137 = v354;
                                      *(_DWORD *)(v68 + 40) = 67;
                                      v363 = (__int64 *)((__int64 (__fastcall *)(_QWORD *, _QWORD *, _QWORD *))unk_142F6A9F0)(
                                                          a1,
                                                          a2: v354,
                                                          a3: v362);
                                      v355 = *v354;
                                      --*v137;
                                      if ( v355 == 1 )
                                        MEMORY[0x13B0039F0](a1: v137);
                                      v80 = (*v362)-- == 1;
                                      if ( v80 )
                                        MEMORY[0x13B0039F0](a1: v362);
                                      if ( v363 == nullptr )
                                      {
                                        v190 = a1[14];
                                        v354 = nullptr;
                                        v191 = 67;
                                        v378 = (_QWORD *)a1[12];
                                        v290 = (_QWORD *)a1[13];
                                        a1[14] = 0;
                                        v381 = v290;
                                        v362 = nullptr;
                                        *((_OWORD *)a1 + 6) = 0;
                                        goto LABEL_281;
                                      }
                                      v362 = (_QWORD *)((__int64 (*)(void))unk_14321A480)();
                                      if ( v362 != nullptr )
                                      {
                                        v362 = (_QWORD *)((__int64 (__fastcall *)(_QWORD *, __int64))unk_1430EC890)(
                                                           a1: v362,
                                                           a2: qword_14393FE60);
                                        if ( v362 == nullptr )
                                        {
LABEL_494:
                                          v190 = a1[14];
                                          v191 = 72;
                                          v378 = (_QWORD *)a1[12];
                                          v286 = (_QWORD *)a1[13];
                                          *((_OWORD *)a1 + 6) = 0;
                                          v381 = v286;
                                          a1[14] = 0;
                                          v354 = nullptr;
                                          goto LABEL_281;
                                        }
                                        v138 = MEMORY[0x13B01B050](a1: v362);
                                        v139 = *v362 - 1LL;
                                        if ( v138 == -1 )
                                        {
                                          v288 = (_QWORD *)a1[12];
                                          v190 = a1[14];
                                          a1[14] = 0;
                                          v378 = v288;
                                          v289 = (_QWORD *)a1[13];
                                          *((_OWORD *)a1 + 6) = 0;
                                          v381 = v289;
                                          *v362 = v139;
                                          if ( v139 == 0 )
                                            MEMORY[0x13B0039F0]();
                                          v191 = 72;
                                          v354 = nullptr;
                                          v362 = nullptr;
                                          goto LABEL_281;
                                        }
                                        *v362 = v139;
                                        if ( v139 == 0 )
                                          MEMORY[0x13B0039F0](a1: v362);
                                        if ( v138 == 0 )
                                        {
                                          ++*(_QWORD *)qword_143A35200;
                                          v362 = (_QWORD *)qword_143A35200;
                                          goto LABEL_174;
                                        }
                                        v284 = ((__int64 (*)(void))unk_14321A480)();
                                        v362 = (_QWORD *)v284;
                                        if ( v284 != 0 )
                                        {
                                          v354 = (_QWORD *)((__int64 (__fastcall *)(__int64, __int64))unk_1430EC890)(
                                                             a1: v284,
                                                             a2: qword_14393FE60);
                                          if ( v354 == nullptr )
                                          {
                                            v190 = a1[14];
                                            v362 = nullptr;
                                            v378 = (_QWORD *)a1[12];
                                            v287 = (_QWORD *)a1[13];
                                            a1[14] = 0;
                                            v191 = 72;
                                            v381 = v287;
                                            *((_OWORD *)a1 + 6) = 0;
                                            goto LABEL_281;
                                          }
                                          v285 = v354;
                                          v362 = (_QWORD *)((__int64 (__fastcall *)(_QWORD *, __int64))unk_1430EC890)(
                                                             a1: v354,
                                                             a2: qword_14393FE68);
                                          v359 = *v354;
                                          --*v285;
                                          if ( v359 == 1 )
                                            MEMORY[0x13B0039F0](a1: v285);
                                          if ( v362 == nullptr )
                                            goto LABEL_494;
LABEL_174:
                                          v354 = (_QWORD *)((__int64 (*)(void))unk_14321A480)();
                                          if ( v354 == nullptr )
                                          {
                                            ((void (__fastcall *)(_QWORD *, _QWORD **, __int64))unk_142F6E530)(
                                              a1,
                                              a2: &a62,
                                              a3: qword_14393FE30);
                                            v191 = 73;
                                            v190 = a64;
                                            v378 = a62;
                                            v381 = a63;
                                            goto LABEL_281;
                                          }
                                          if ( (unsigned __int8)((__int64 (__fastcall *)(_QWORD *, __int64, _QWORD *))unk_1430FA9F0)(
                                                                  a1: v354,
                                                                  a2: qword_14393FE60,
                                                                  a3: v365) == 0 )
                                          {
                                            v190 = a1[14];
                                            v191 = 73;
                                            v378 = (_QWORD *)a1[12];
                                            v283 = (_QWORD *)a1[13];
                                            *((_OWORD *)a1 + 6) = 0;
                                            v381 = v283;
                                            a1[14] = 0;
                                            v354 = nullptr;
                                            goto LABEL_281;
                                          }
                                          v140 = ((__int64 (*)(void))unk_14321A5D0)();
                                          v354 = (_QWORD *)v140;
                                          if ( v140 == 0 )
                                          {
                                            ((void (__fastcall *)(_QWORD *, _QWORD **, __int64))unk_142F6E530)(
                                              a1,
                                              a2: &a62,
                                              a3: qword_14393FE70);
                                            v191 = 74;
                                            v190 = a64;
                                            v378 = a62;
                                            v381 = a63;
                                            goto LABEL_281;
                                          }
                                          *(_DWORD *)(v68 + 40) = 74;
                                          v141 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64))unk_1430D8EF0)(
                                                   a1,
                                                   a2: v140,
                                                   a3: qword_14393FE70);
                                          if ( v141 == 0 )
                                          {
                                            v190 = a1[14];
                                            v191 = 74;
                                            v378 = (_QWORD *)a1[12];
                                            v282 = (_QWORD *)a1[13];
                                            *((_OWORD *)a1 + 6) = 0;
                                            v381 = v282;
                                            a1[14] = 0;
                                            v354 = nullptr;
                                            goto LABEL_281;
                                          }
                                          v379 = (_QWORD *)v141;
                                          v142 = ((__int64 (*)(void))unk_14321A480)();
                                          v354 = (_QWORD *)v142;
                                          if ( v142 == 0 )
                                          {
                                            ((void (__fastcall *)(_QWORD *, _QWORD **, __int64))unk_142F6E530)(
                                              a1,
                                              a2: &a62,
                                              a3: qword_14393FE30);
                                            v191 = 74;
                                            v280 = v379;
                                            v190 = a64;
                                            v378 = a62;
                                            v281 = a63;
                                            v80 = (*v379)-- == 1;
                                            v381 = v281;
                                            if ( v80 )
                                            {
                                              MEMORY[0x13B0039F0](a1: v280);
                                              v191 = 74;
                                            }
                                            goto LABEL_281;
                                          }
                                          v143 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD *))unk_1430FA9F0)(
                                                   a1: v142,
                                                   a2: qword_14393FE78,
                                                   a3: v379);
                                          v80 = (*v379)-- == 1;
                                          if ( v80 )
                                            MEMORY[0x13B0039F0](a1: v379);
                                          if ( v143 == 0 )
                                          {
                                            v278 = (_QWORD *)a1[12];
                                            v190 = a1[14];
                                            v191 = 74;
                                            a1[14] = 0;
                                            v378 = v278;
                                            v279 = (_QWORD *)a1[13];
                                            *((_OWORD *)a1 + 6) = 0;
                                            v381 = v279;
                                            v354 = nullptr;
                                            goto LABEL_281;
                                          }
                                          v354 = (_QWORD *)((__int64 (*)(void))unk_14321A480)();
                                          if ( v354 == nullptr )
                                          {
                                            ((void (__fastcall *)(_QWORD *, _QWORD **, __int64))unk_142F6E530)(
                                              a1,
                                              a2: &a62,
                                              a3: qword_14393FE30);
                                            v191 = 75;
                                            v190 = a64;
                                            v378 = a62;
                                            v381 = a63;
                                            goto LABEL_281;
                                          }
                                          *(_DWORD *)(v68 + 40) = 75;
                                          v354 = (_QWORD *)((__int64 (__fastcall *)(_QWORD *, _QWORD *, __int64))unk_1430D8EF0)(
                                                             a1,
                                                             a2: v354,
                                                             a3: qword_14393FE80);
                                          if ( v354 == nullptr )
                                          {
                                            v276 = (_QWORD *)a1[12];
                                            v190 = a1[14];
                                            v191 = 75;
                                            a1[14] = 0;
                                            v378 = v276;
                                            v277 = (_QWORD *)a1[13];
                                            *((_OWORD *)a1 + 6) = 0;
                                            v381 = v277;
                                            goto LABEL_281;
                                          }
                                          v144 = v354;
                                          v356 = *v354;
                                          *v144 = v356 - 1;
                                          if ( v356 == 1 )
                                            MEMORY[0x13B0039F0](a1: v144);
                                          v354 = (_QWORD *)((__int64 (*)(void))unk_14321A5D0)();
                                          if ( v354 == nullptr )
                                          {
                                            ((void (__fastcall *)(_QWORD *, _QWORD **, __int64))unk_142F6E530)(
                                              a1,
                                              a2: &a62,
                                              a3: qword_14393FE70);
                                            v191 = 76;
                                            v190 = a64;
                                            v378 = a62;
                                            v381 = a63;
                                            goto LABEL_281;
                                          }
                                          *(_DWORD *)(v68 + 40) = 76;
                                          v354 = (_QWORD *)((__int64 (__fastcall *)(_QWORD *, _QWORD *, __int64, _QWORD))unk_1430D9050)(
                                                             a1,
                                                             a2: v354,
                                                             a3: qword_14393FE88,
                                                             a4: *(_QWORD *)(qword_14393FE90 + 24));
                                          if ( v354 == nullptr )
                                          {
                                            v274 = (_QWORD *)a1[12];
                                            v190 = a1[14];
                                            v191 = 76;
                                            a1[14] = 0;
                                            v378 = v274;
                                            v275 = (_QWORD *)a1[13];
                                            *((_OWORD *)a1 + 6) = 0;
                                            v381 = v275;
                                            goto LABEL_281;
                                          }
                                          v380 = MEMORY[0x13B135D60](a1: qword_14393FD38);
                                          v146 = *(_QWORD *)(*(_QWORD *)&qword_14393FD08[0] + 32LL);
                                          if ( *(_BYTE *)(v146 + 10) != 0 )
                                          {
                                            v147 = *(_DWORD *)(v146 + 12);
                                            if ( v147 == 0 )
                                            {
                                              v147 = dword_143547A4C;
                                              *(_DWORD *)(v146 + 12) = dword_143547A4C++;
                                            }
                                            if ( dword_143547A48 != v147 )
                                            {
                                              v382 = v146;
                                              dword_143547A48 = v147;
                                              v148 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
                                                       a1: v146,
                                                       a2: qword_14393FE98,
                                                       a3: *(_QWORD *)(qword_14393FE98 + 24));
                                              v146 = v382;
                                              qword_143944138 = v148;
                                            }
                                            if ( qword_143944138 >= 0 )
                                            {
                                              v149 = v146 + (1LL << *(_BYTE *)(v146 + 9)) + 32;
                                              v150 = *(_QWORD *)(v149 + 16 * qword_143944138 + 8);
                                              if ( v150 != 0 )
                                                goto LABEL_195;
                                              v256 = ((__int64 (__fastcall *)(__int64, __int64, _QWORD))unk_142F57240)(
                                                       a1: v146,
                                                       a2: qword_14393FE98,
                                                       a3: *(_QWORD *)(qword_14393FE98 + 24));
                                              qword_143944138 = v256;
                                              if ( v256 >= 0 )
                                              {
                                                v150 = *(_QWORD *)(v149 + 16 * v256 + 8);
                                                goto LABEL_446;
                                              }
                                            }
                                          }
                                          else
                                          {
                                            v258 = (__int64 *)MEMORY[0x13B02A410](
                                                                a1: *(_QWORD *)&qword_14393FD08[0],
                                                                a2: qword_14393FE98);
                                            if ( v258 != nullptr )
                                            {
                                              v150 = *v258;
LABEL_446:
                                              if ( v150 != 0 )
                                                goto LABEL_195;
                                            }
                                          }
                                          v257 = (__int64 *)MEMORY[0x13B02A410](
                                                              a1: *(_QWORD *)qword_1435FA560,
                                                              a2: qword_14393FE98,
                                                              a3: v145,
                                                              a4: v146);
                                          if ( v257 == nullptr || (v150 = *v257, *v257 == 0) )
                                          {
                                            ((void (__fastcall *)(_QWORD *, _QWORD **, __int64))unk_142F6E530)(
                                              a1,
                                              a2: &a62,
                                              a3: qword_14393FE98);
                                            v191 = 77;
                                            v190 = a64;
                                            v378 = a62;
                                            v381 = a63;
                                            goto LABEL_281;
                                          }
LABEL_195:
                                          *(_DWORD *)(v68 + 40) = 77;
                                          v151 = ((__int64 (__fastcall *)(_QWORD *, __int64, __int64))unk_142F78640)(
                                                   a1,
                                                   a2: v150,
                                                   a3: qword_14393FEA0);
                                          if ( v151 != 0 )
                                          {
                                            v383 = (_QWORD *)v151;
                                            v152 = (_QWORD *)((__int64 (__fastcall *)(__int64, __int64))unk_1430EC890)(
                                                               a1: v151,
                                                               a2: qword_14393FEA8);
                                            v80 = (*v383)-- == 1;
                                            if ( v80 )
                                              MEMORY[0x13B0039F0]();
                                            if ( v152 != nullptr )
                                            {
                                              *(_DWORD *)(v68 + 40) = 77;
                                              a62 = v354;
                                              v153 = ((__int64 (__fastcall *)(_QWORD *, _QWORD *, _QWORD **, __int64))unk_1430D4C80)(
                                                       a1,
                                                       a2: v152,
                                                       a3: &a62,
                                                       a4: qword_14393FEB0);
                                              v80 = (*v152)-- == 1;
                                              v155 = (_QWORD *)v153;
                                              if ( v80 )
                                              {
                                                v384 = v153;
                                                MEMORY[0x13B0039F0](a1: v152, a2: v154, a3: v153);
                                                v155 = (_QWORD *)v384;
                                              }
                                              if ( v155 != nullptr )
                                              {
                                                *(_DWORD *)(v68 + 40) = 77;
                                                v385 = v155;
                                                v156 = (_QWORD *)((__int64 (__fastcall *)(_QWORD *, __int64))unk_142F6A9F0)(
                                                                   a1,
                                                                   a2: v380);
                                                v80 = (*v385)-- == 1;
                                                if ( v80 )
                                                  MEMORY[0x13B0039F0](a1: v385);
                                                if ( v156 != nullptr )
                                                {
                                                  v80 = (*v156)-- == 1;
                                                  if ( v80 )
                                                    MEMORY[0x13B0039F0](a1: v156);
                                                  v157 = ((__int64 (*)(void))unk_14321A480)();
                                                  if ( v157 == 0 )
                                                  {
                                                    ((void (__fastcall *)(_QWORD *, _QWORD **, __int64))unk_142F6E530)(
                                                      a1,
                                                      a2: &a62,
                                                      a3: qword_14393FE30);
                                                    v191 = 78;
                                                    v190 = a64;
                                                    v378 = a62;
                                                    v381 = a63;
                                                    goto LABEL_281;
                                                  }
                                                  v158 = ((__int64 (__fastcall *)(__int64, __int64))unk_1430EC890)(
                                                           a1: v157,
                                                           a2: qword_14393FE60);
                                                  if ( v158 != 0 )
                                                  {
                                                    v375 = (_QWORD *)v158;
                                                    v159 = (_QWORD *)((__int64 (__fastcall *)(__int64, __int64))unk_1430EC890)(
                                                                       a1: v158,
                                                                       a2: qword_14393FE68);
                                                    v80 = (*v375)-- == 1;
                                                    if ( v80 )
                                                      MEMORY[0x13B0039F0]();
                                                    if ( v159 != nullptr )
                                                    {
                                                      v160 = ((__int64 (__fastcall *)(_QWORD *, _QWORD *))unk_1430EBE90)(
                                                               a1: v362,
                                                               a2: v159);
                                                      v80 = (*v159)-- == 1;
                                                      if ( v80 )
                                                      {
                                                        v376 = v160;
                                                        MEMORY[0x13B0039F0](a1: v159);
                                                        v160 = v376;
                                                      }
                                                      if ( v160 != 0 )
                                                      {
                                                        v377 = (_QWORD *)v160;
                                                        ((void (__fastcall *)(_QWORD))unk_143526460)(a1: a1[7]);
                                                        result = v377;
                                                        ++*v377;
                                                        v162 = *a35 - 1;
                                                        *a35 = v162;
                                                        if ( v162 == 0 )
                                                        {
                                                          MEMORY[0x13B0039F0](a1: a35);
                                                          result = v377;
                                                        }
                                                        v80 = (*v66)-- == 1;
                                                        if ( v80 )
                                                        {
                                                          v302 = result;
                                                          MEMORY[0x13B0039F0](a1: v66);
                                                          result = v302;
                                                        }
                                                        v80 = (*v75)-- == 1;
                                                        if ( v80 )
                                                        {
                                                          v303 = result;
                                                          MEMORY[0x13B0039F0](a1: v75);
                                                          result = v303;
                                                        }
                                                        v80 = (*v64)-- == 1;
                                                        if ( v80 )
                                                        {
                                                          v304 = result;
                                                          MEMORY[0x13B0039F0](a1: v64);
                                                          result = v304;
                                                        }
                                                        v80 = (*v67)-- == 1;
                                                        if ( v80 )
                                                        {
                                                          v305 = result;
                                                          MEMORY[0x13B0039F0](a1: v67);
                                                          result = v305;
                                                        }
                                                        v80 = (*v65)-- == 1;
                                                        if ( v80 )
                                                        {
                                                          v306 = result;
                                                          MEMORY[0x13B0039F0](a1: v65);
                                                          result = v306;
                                                        }
                                                        v163 = *a36 - 1LL;
                                                        *a36 = v163;
                                                        if ( v163 == 0 )
                                                        {
                                                          v307 = result;
                                                          MEMORY[0x13B0039F0](a1: a36);
                                                          result = v307;
                                                        }
                                                        v164 = *v333 - 1LL;
                                                        *v333 = v164;
                                                        if ( v164 == 0 )
                                                        {
                                                          v308 = result;
                                                          MEMORY[0x13B0039F0](a1: v333);
                                                          result = v308;
                                                        }
                                                        v165 = *v335 - 1LL;
                                                        *v335 = v165;
                                                        if ( v165 == 0 )
                                                        {
                                                          v309 = result;
                                                          MEMORY[0x13B0039F0](a1: v335);
                                                          result = v309;
                                                        }
                                                        v166 = *v337 - 1LL;
                                                        *v337 = v166;
                                                        if ( v166 == 0 )
                                                        {
                                                          v310 = result;
                                                          MEMORY[0x13B0039F0](a1: v337);
                                                          result = v310;
                                                        }
                                                        v167 = *v339 - 1LL;
                                                        *v339 = v167;
                                                        if ( v167 == 0 )
                                                        {
                                                          v311 = result;
                                                          MEMORY[0x13B0039F0](a1: v339);
                                                          result = v311;
                                                        }
                                                        v168 = *v341 - 1LL;
                                                        *v341 = v168;
                                                        if ( v168 == 0 )
                                                        {
                                                          v312 = result;
                                                          MEMORY[0x13B0039F0](a1: v341);
                                                          result = v312;
                                                        }
                                                        v169 = *v346 - 1LL;
                                                        *v346 = v169;
                                                        if ( v169 == 0 )
                                                        {
                                                          v313 = result;
                                                          MEMORY[0x13B0039F0](a1: v346);
                                                          result = v313;
                                                        }
                                                        v170 = *v343 - 1LL;
                                                        *v343 = v170;
                                                        if ( v170 == 0 )
                                                        {
                                                          v314 = result;
                                                          MEMORY[0x13B0039F0](a1: v343);
                                                          result = v314;
                                                        }
                                                        v171 = *v347 - 1LL;
                                                        *v347 = v171;
                                                        if ( v171 == 0 )
                                                        {
                                                          v315 = result;
                                                          MEMORY[0x13B0039F0](a1: v347);
                                                          result = v315;
                                                        }
                                                        v172 = *v364 - 1LL;
                                                        *v364 = v172;
                                                        if ( v172 == 0 )
                                                        {
                                                          v316 = result;
                                                          MEMORY[0x13B0039F0](a1: v364);
                                                          result = v316;
                                                        }
                                                        v173 = *v371 - 1LL;
                                                        *v371 = v173;
                                                        if ( v173 == 0 )
                                                        {
                                                          v317 = result;
                                                          MEMORY[0x13B0039F0](a1: v371);
                                                          result = v317;
                                                        }
                                                        v174 = *v374 - 1LL;
                                                        *v374 = v174;
                                                        if ( v174 == 0 )
                                                        {
                                                          v318 = result;
                                                          MEMORY[0x13B0039F0](a1: v374);
                                                          result = v318;
                                                        }
                                                        v175 = *v373 - 1;
                                                        *v373 = v175;
                                                        if ( v175 == 0 )
                                                        {
                                                          v319 = result;
                                                          MEMORY[0x13B0039F0](a1: v373);
                                                          result = v319;
                                                        }
                                                        v176 = *v372 - 1;
                                                        *v372 = v176;
                                                        if ( v176 == 0 )
                                                        {
                                                          v320 = result;
                                                          MEMORY[0x13B0039F0](a1: v372);
                                                          result = v320;
                                                        }
                                                        v177 = *v370 - 1;
                                                        *v370 = v177;
                                                        if ( v177 == 0 )
                                                        {
                                                          v321 = result;
                                                          MEMORY[0x13B0039F0](a1: v370);
                                                          result = v321;
                                                        }
                                                        v178 = *v368 - 1;
                                                        *v368 = v178;
                                                        if ( v178 == 0 )
                                                        {
                                                          v322 = result;
                                                          MEMORY[0x13B0039F0](a1: v368);
                                                          result = v322;
                                                        }
                                                        v179 = *v369 - 1;
                                                        *v369 = v179;
                                                        if ( v179 == 0 )
                                                        {
                                                          v323 = result;
                                                          MEMORY[0x13B0039F0](a1: v369);
                                                          result = v323;
                                                        }
                                                        v180 = *v367 - 1;
                                                        *v367 = v180;
                                                        if ( v180 == 0 )
                                                        {
                                                          v324 = result;
                                                          MEMORY[0x13B0039F0](a1: v367);
                                                          result = v324;
                                                        }
                                                        v181 = *v365 - 1LL;
                                                        *v365 = v181;
                                                        if ( v181 == 0 )
                                                        {
                                                          v325 = result;
                                                          MEMORY[0x13B0039F0](a1: v365);
                                                          result = v325;
                                                        }
                                                        v182 = *v366 - 1;
                                                        *v366 = v182;
                                                        if ( v182 == 0 )
                                                        {
                                                          v326 = result;
                                                          MEMORY[0x13B0039F0](a1: v366);
                                                          result = v326;
                                                        }
                                                        v183 = *v363 - 1;
                                                        *v363 = v183;
                                                        if ( v183 == 0 )
                                                        {
                                                          v327 = result;
                                                          MEMORY[0x13B0039F0](a1: v363);
                                                          result = v327;
                                                        }
                                                        v184 = *v362 - 1LL;
                                                        *v362 = v184;
                                                        if ( v184 == 0 )
                                                        {
                                                          v328 = result;
                                                          MEMORY[0x13B0039F0](a1: v362);
                                                          result = v328;
                                                        }
                                                        v185 = *v354 - 1LL;
                                                        *v354 = v185;
                                                        if ( v185 == 0 )
                                                        {
                                                          v329 = result;
                                                          MEMORY[0x13B0039F0](a1: v354);
                                                          result = v329;
                                                        }
                                                        v80 = (*result)-- == 1;
                                                        if ( v80 )
                                                        {
                                                          v330 = result;
                                                          MEMORY[0x13B0039F0](a1: result);
                                                          result = v330;
                                                        }
                                                        v186 = v299;
                                                        v187 = *v299 - 1;
                                                        *v299 = v187;
                                                        if ( v187 == 0 )
                                                        {
                                                          v300 = result;
                                                          MEMORY[0x13B0039F0](a1: v186);
                                                          return v300;
                                                        }
                                                        return result;
                                                      }
                                                    }
                                                  }
                                                  v259 = (_QWORD *)a1[12];
                                                  v190 = a1[14];
                                                  v191 = 78;
                                                  a1[14] = 0;
                                                  v378 = v259;
                                                  v260 = (_QWORD *)a1[13];
                                                  *((_OWORD *)a1 + 6) = 0;
                                                  v381 = v260;
                                                  goto LABEL_281;
                                                }
                                              }
                                            }
                                          }
                                          v254 = (_QWORD *)a1[12];
                                          v190 = a1[14];
                                          v191 = 77;
                                          a1[14] = 0;
                                          v378 = v254;
                                          v255 = (_QWORD *)a1[13];
                                          *((_OWORD *)a1 + 6) = 0;
                                          v381 = v255;
                                          goto LABEL_281;
                                        }
                                      }
                                      ((void (__fastcall *)(_QWORD *, _QWORD **, __int64))unk_142F6E530)(
                                        a1,
                                        a2: &a62,
                                        a3: qword_14393FE30);
                                      v190 = a64;
                                      v354 = nullptr;
                                      v191 = 72;
                                      v378 = a62;
                                      v381 = a63;
                                      goto LABEL_281;
                                    }
                                  }
                                  v190 = a1[14];
                                  v191 = 53;
                                  v378 = (_QWORD *)a1[12];
                                  v252 = (_QWORD *)a1[13];
                                  *((_OWORD *)a1 + 6) = 0;
                                  v381 = v252;
                                  a1[14] = 0;
                                  v354 = nullptr;
                                  v362 = nullptr;
                                  v363 = nullptr;
                                  v366 = nullptr;
                                  v365 = nullptr;
                                  v367 = nullptr;
                                  v369 = nullptr;
                                  goto LABEL_281;
                                }
                              }
                              v190 = a1[14];
                              v191 = 52;
                              v378 = (_QWORD *)a1[12];
                              v250 = (_QWORD *)a1[13];
                              *((_OWORD *)a1 + 6) = 0;
                              v381 = v250;
                              a1[14] = 0;
                              v354 = nullptr;
                              v362 = nullptr;
                              v363 = nullptr;
                              v366 = nullptr;
                              v365 = nullptr;
                              v367 = nullptr;
                              v369 = nullptr;
                              v368 = nullptr;
                              goto LABEL_281;
                            }
                          }
                          v190 = a1[14];
                          v354 = nullptr;
                          v191 = 51;
                          v378 = (_QWORD *)a1[12];
                          v248 = (_QWORD *)a1[13];
                          a1[14] = 0;
                          v381 = v248;
                          v362 = nullptr;
                          v363 = nullptr;
                          v366 = nullptr;
                          v365 = nullptr;
                          v367 = nullptr;
                          v369 = nullptr;
                          v368 = nullptr;
                          v370 = nullptr;
                          *((_OWORD *)a1 + 6) = 0;
                          goto LABEL_281;
                        }
                      }
                      v190 = a1[14];
                      v354 = nullptr;
                      v191 = 50;
                      v378 = (_QWORD *)a1[12];
                      v246 = (_QWORD *)a1[13];
                      a1[14] = 0;
                      v381 = v246;
                      v362 = nullptr;
                      v363 = nullptr;
                      v366 = nullptr;
                      v365 = nullptr;
                      v367 = nullptr;
                      v369 = nullptr;
                      v368 = nullptr;
                      v370 = nullptr;
                      v372 = nullptr;
                      *((_OWORD *)a1 + 6) = 0;
                      goto LABEL_281;
                    }
                  }
                  v190 = a1[14];
                  v354 = nullptr;
                  v191 = 49;
                  v378 = (_QWORD *)a1[12];
                  v244 = (_QWORD *)a1[13];
                  a1[14] = 0;
                  v381 = v244;
                  v362 = nullptr;
                  v363 = nullptr;
                  v366 = nullptr;
                  v365 = nullptr;
                  v367 = nullptr;
                  v369 = nullptr;
                  v368 = nullptr;
                  v370 = nullptr;
                  v372 = nullptr;
                  v373 = nullptr;
                  *((_OWORD *)a1 + 6) = 0;
                  goto LABEL_281;
                }
              }
              v190 = a1[14];
              v191 = 47;
              v378 = (_QWORD *)a1[12];
              v242 = (_QWORD *)a1[13];
              *((_OWORD *)a1 + 6) = 0;
              v381 = v242;
              a1[14] = 0;
              v354 = nullptr;
              v362 = nullptr;
              v363 = nullptr;
              v366 = nullptr;
              v365 = nullptr;
              v367 = nullptr;
              v369 = nullptr;
              v368 = nullptr;
              v370 = nullptr;
              v372 = nullptr;
              v373 = nullptr;
              v374 = nullptr;
              goto LABEL_281;
            }
          }
          v240 = (_QWORD *)a1[12];
          v190 = a1[14];
          v354 = nullptr;
          a1[14] = 0;
          v191 = 46;
          v378 = v240;
          v362 = nullptr;
          v381 = (_QWORD *)a1[13];
          v363 = nullptr;
          v366 = nullptr;
          v365 = nullptr;
          v367 = nullptr;
          v369 = nullptr;
          v368 = nullptr;
          v370 = nullptr;
          v372 = nullptr;
          v373 = nullptr;
          v374 = nullptr;
          v371 = nullptr;
          *((_OWORD *)a1 + 6) = 0;
          goto LABEL_281;
        }
      }
      v238 = (_QWORD *)a1[12];
      v190 = a1[14];
      v354 = nullptr;
      a1[14] = 0;
      v191 = 45;
      v378 = v238;
      v362 = nullptr;
      v381 = (_QWORD *)a1[13];
      v363 = nullptr;
      v366 = nullptr;
      v365 = nullptr;
      v367 = nullptr;
      v369 = nullptr;
      v368 = nullptr;
      v370 = nullptr;
      v372 = nullptr;
      v373 = nullptr;
      v374 = nullptr;
      v371 = nullptr;
      v364 = nullptr;
      *((_OWORD *)a1 + 6) = 0;
      goto LABEL_281;
    }
  }
  v234 = (_QWORD *)a1[12];
  v190 = a1[14];
  v354 = nullptr;
  a1[14] = 0;
  v191 = 44;
  v378 = v234;
  v362 = nullptr;
  v381 = (_QWORD *)a1[13];
  v363 = nullptr;
  v366 = nullptr;
  v365 = nullptr;
  v367 = nullptr;
  v369 = nullptr;
  v368 = nullptr;
  v370 = nullptr;
  v372 = nullptr;
  v373 = nullptr;
  v374 = nullptr;
  v371 = nullptr;
  v364 = nullptr;
  v347 = nullptr;
  *((_OWORD *)a1 + 6) = 0;
  goto LABEL_281;
}