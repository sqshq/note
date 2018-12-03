---
title: Lab1 Data Lab
toc: true
date: 2017-12-30
tags: [CSAPP]
top: 1
---



#### 位操作

bitXor - x^y using only ~ and & 

* Example: bitXor(4, 5) = 1
* Legal ops: ~ &
* Max ops: 14

```C
int bitXor(int x, int y) {
  return ~(x&y)&(~((~x)&(~y)));
}
```

allOddBits - return 1 if all odd-numbered bits in word set to 1

* Examples allOddBits(0xFFFFFFFD) = 0, allOddBits(0xAAAAAAAA) = 1
* Legal ops: ! ~ & ^ | + << >>
* Max ops: 12

```C
int allOddBits(int x) {
  int v = 0xAA;
  v = v | (v << 8);
  v = v | (v << 16);
  return !(((x & v) | (~v)) +1);
}
```

isAsciiDigit - return 1 if 0x30 <= x <= 0x39 (ASCII codes for characters '0' to '9')

* Example: isAsciiDigit(0x35) = 1. isAsciiDigit(0x3a) = 0. isAsciiDigit(0x05) = 0.
* Legal ops: ! ~ & ^ | + << >>
* Max ops: 15

```C
int isAsciiDigit(int x) {
  return  (!(~(x >> 8)+1))&(!((x-0x30)>>31))&(!(((x-0x3a)>>31)+1));
}
```

conditional - same as x ? y : z 

* Example: conditional(2,4,5) = 4
* Legal ops: ! ~ & ^ | + << >>
* Max ops: 16

```C
// repeat
int conditional(int x, int y, int z) {
  /*
     *if x!=0,mask=0x00000000, y&~mask=y and z&mask=0
     *if x==0,mask=0xffffffff, y&~mask = y&0 =0; z&mask=z
  */
  int mask= ~!x+1; 
  return (y & ~mask)|(z & mask);
}
```

logicalNeg - implement the ! operator, using all of the legal operators except !

* Examples: logicalNeg(3) = 0, logicalNeg(0) = 1
* Legal ops: ~ & ^ | + << >>
* Max ops: 12

```C
int logicalNeg(int x) {
  return !(~(x-1));
}
```

#### 补码运算


tmin - return minimum two's complement integer 

* Legal ops: ! ~ & ^ | + << >>
* Max ops: 4


```C
int tmin(void) {
  return 1<<31;
}
```

isTmax - returns 1 if x is the maximum, two's complement number, and 0 otherwise 

* Legal ops: ! ~ & ^ | +
* Max ops: 10


```C
int isTmax(int x) {
  return !((~x) ^ (x + 1)) & !!(~x);
}
```

negate - return -x 

* Example: negate(1) = -1.
* Legal ops: ! ~ & ^ | + << >>
* Max ops: 5

```C
int negate(int x) {
  return ~(x-1);
}
```


isLessOrEqual - if x <= y  then return 1, else return 0 

* Example: isLessOrEqual(4,5) = 1.
* Legal ops: ! ~ & ^ | + << >>
* Max ops: 24


```C
int isLessOrEqual(int x, int y) {
  return (!(((x-y)>>31)+1)) || (!(x-y));
}
```

howManyBits - return the minimum number of bits required to represent x in two's complement

* Examples: howManyBits(12) = 5, howManyBits(298) = 10, howManyBits(-5) = 4, howManyBits(0)  = 1, howManyBits(-1) = 1, howManyBits(0x80000000) = 32
* Legal ops: ! ~ & ^ | + << >>
* Max ops: 90
* Rating: 4

```C
int howManyBits(int x) {
  return 4;
}
```

#### 浮点数运算

float_twice - Return bit-level equivalent of expression 2*f for
floating point argument f.

* Both the argument and result are passed as unsigned int's, but they are to be interpreted as the bit-level representation of single-precision floating point values.
* When argument is NaN, return argument
* Legal ops: Any integer/unsigned operations incl. ||, &&. also if, while
Max ops: 30

```C
unsigned float_twice(unsigned uf) {
  unsigned sign = uf & 0x80000000;
  unsigned exp = uf & 0x7f800000;
  unsigned frac = uf & 0x007FFFFF;

    if (exp==0x7F800000) // when argument is NaN, return argument
      return uf;

    if (exp == 0x0) // 无规格化的情况
      return sign | (frac << 1);

    if (exp == 0x7f000000)// 会变成无穷大
      frac = 0x0;

    return sign|(exp+0x800000)|frac;
  }
```

float_i2f - Return bit-level equivalent of expression (float) x
Result is returned as unsigned int, but

* it is to be interpreted as the bit-level representation of a single-precision floating point values.
* Legal ops: Any integer/unsigned operations incl. ||, &&. also if, while
* Max ops: 30

```C
  unsigned float_i2f(int x) {
    //Rounding is important!  
    unsigned sign=0,shiftleft=0,flag=0,tmp;  
    unsigned absx=x;  
    if( x==0 ) return 0;  
    if( x<0 ){  
     sign=0x80000000;  
     absx=-x;  
   }  
  while(1){//Shift until the highest bit equal to 1 in order to normalize the floating-point number  
   tmp=absx;  
   absx<<=1;  
   shiftleft++;  
   if( tmp&0x80000000 ) break;  
 }  

 //round to even
  if( (absx & 0x01ff) > 0x0100 ) flag=1;//向上舍入
  if( (absx & 0x03ff) == 0x0300 ) flag=1;//中间值，向偶数舍入

  return sign+(absx>>9)+((159-shiftleft)<<23)+flag;  
}
```


float_f2i - Return bit-level equivalent of expression (int) f
for floating point argument f.

* Argument is passed as unsigned int, but it is to be interpreted as the bit-level representation of a single-precision floating point value.
* Anything out of range (including NaN and infinity) should return 0x80000000u.
* Legal ops: Any integer/unsigned operations incl. ||, &&. also if, while
* Max ops: 30


```C
int float_f2i(unsigned uf) {
  int sign = (uf>>31)==0 ? 1: -1; //最高位
  int exp  = uf&0x7f800000;  //中间8位
  unsigned frac = uf&0x007FFFFF; //最低23位

  //特殊情况NaN, inf
  if (exp==0x7f800000)
    return 0x80000000u;

  //特殊情况：0
  if (uf==0x800000)
    return 0;

  //非规格化
  if (exp==0)
    exp = 1-127; //1-bias
  else
  //规格化
  {
    exp = (exp>>23)-127;// exp-bias;
    frac = 1+frac; // frac+=1;
  }

  // 如果小于0.5, 那么应该等于0
  if (exp < -1)
    return 0;

  return sign * (frac << exp);
}
```