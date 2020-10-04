/*	example code for cc65, for NES
 *  draw a BG with metatile system
 *	, also sprite collisions with BG
 *	using neslib
 *	Doug Fraker 2018
 */	
 

#include "LIB/neslib.h"
#include "LIB/nesdoug.h"
#include "Sprites.h" // holds our metasprite data
#include "metatiles.h"
	
void main (void) {
	
	ppu_off(); // screen off
	
	// load the palettes
	pal_bg(palette_bg);

	// use the second set of tiles for sprites
	// both bg and sprites are set to 0 by default
	bank_spr(1);

	set_vram_buffer(); // do at least once, sets a pointer to a buffer
	clear_vram_buffer();

	load_room();
	
	ppu_on_all(); // turn on screen
	
	while (1)
    {
    }
}

void load_room(void){
	set_data_pointer(Room1);
	set_mt_pointer(metatiles1);
	for(y=0; ;y+=0x20){
		for(x=0; ;x+=0x20){
			clear_vram_buffer(); // do each frame, and before putting anything in the buffer
			address = get_ppu_addr(0, x, y);
			index = (y & 0xf0) + (x >> 4);
			buffer_4_mt(address, index); // ppu_address, index to the data
			flush_vram_update_nmi();
			if (x == 0xe0) break;
		}
		if (y == 0xe0) break;
	}
	
	set_vram_update(NULL); // just turn ppu updates OFF for this example
}

