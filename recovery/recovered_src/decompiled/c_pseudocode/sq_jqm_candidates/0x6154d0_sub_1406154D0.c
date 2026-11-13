void __fastcall sub_1406154D0(__int64 a1)
{
  __int64 v1; // rax
  _QWORD *v2; // rbx
  __int64 v3; // rbp
  __int64 v4; // rdx
  unsigned __int64 v5; // r8
  __int128 v6; // xmm0
  __int64 v7; // rax

  *(_DWORD *)(v3 + 24) = (_DWORD)v2;
  ++*v2;
  *(_QWORD *)(v3 + 32) = v1;
  v4 = *(_QWORD *)(*(_QWORD *)(*(_QWORD *)(qword_143A35A28 + 504) + 16LL) + 744LL);
  v5 = *(_QWORD *)(v4 + 8);
  *(_QWORD *)&v6 = v4;
  v7 = v5 | *(_QWORD *)(v3 - 8) & 3LL;
  *(_QWORD *)v5 = a1;
  *((_QWORD *)&v6 + 1) = v7;
  *(_OWORD *)(v3 - 16) = v6;
  *(_QWORD *)(v4 + 8) = a1;
  JUMPOUT(0x140615358LL);
}