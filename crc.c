/* filename: pi.c*/
# include <stdlib.h>
# include <math.h>

/* Returns a very crude approximation of Pi
   given a int: a number of iteration */
float pi_approx(int n){

  double i,x,y,sum=0;

  for(i=0;i<n;i++){

    x=rand();
    y=rand();

    if (sqrt(x*x+y*y) < sqrt((double)RAND_MAX*RAND_MAX))
      sum++; }

  return 4*(float)sum/(float)n; }


// Subroutine used by get_crc16z function
u_int16_t crc16_update ( u_int16_t crc, u_int8_t data )
{
	u_int16_t ret_val;
	data ^= (u_int8_t)(crc) & (u_int8_t)(0xFF);
	data ^= data << 4;
	ret_val = ((((u_int16_t)data << 8) | ((crc & 0xFF00) >> 8))
		^ (u_int8_t)(data >> 4)
		^ ((u_int16_t)data << 3));
	return ret_val;
}
// -----------------------------------------------------------//
// -----------------------------------------------------------//
// Function to compute CRC16:
// *p : pointer to first data byte
// len: Number of data bytes
// return value is CRC16 over source data p[0]… p[len-1]
u_int16_t get_crc16z(u_int8_t *p, u_int16_t len)
{
	u_int16_t crc16_data=0;
	while(len--)
	{
		crc16_data = crc16_update(crc16_data, p[0]);
		p++;
	}
	return(crc16_data);
}
