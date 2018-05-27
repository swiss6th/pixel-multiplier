# Pixel Multiplier

Pixel Multiplier is a utility to take an arbitrary number of RGB pixel values (3 DMX channels each) and multiply them live. It is written in Python and requires [Open Lighting Architecture](https://openlighting.org/ola/).

## Use Cases

I wrote Pixel Multiplier because I needed a way to use a mobile phone screen as a DMX-controlled light source. There is an app on iOS called [iLedMapper](https://itunes.apple.com/us/app/iledmapper/id404442976?mt=8), but it does not allow for the whole screen to be addressed as one pixel. Since my single DMX universe is already quite full, I needed to minimize the number of channels required to accomplish this. Thus, I wrote Pixel Multiplier. Now I can use a handful of iOS device screens as practical effects on stage.

## Setup

These instructions assume you're setting up Pixel Multiplier on a Raspberry Pi as a part of [Attacca DMX](https://github.com/swiss6th/attacca-dmx), as I have. You'll need to adapt this slightly if you're running on a different platform or running without Attacca DMX. For example, take out the references to `olat.target` in the `systemd` unit if you're not using Attacca DMX.

1. Copy `pixel_multiplier.py` to `/usr/local/bin`, renaming to `pixel_multiplier`.

1. Run `sudo chmod a+x /usr/local/bin/pixel_multiplier`.

1. Copy `pixel_multiplier.environment` and `pixel_multiplier.conf` to `/home/pi`.

1. Set up your pixel routings in [pixel_multiplier.conf](https://github.com/swiss6th/pixel-multiplier/blob/master/home/pi/pixel_multiplier.conf). See comments and examples in that file for details.

1. Copy `pixel_multiplier.service` to `/etc/systemd/system`.

1. Run `sudo systemctl daemon-reload`.

1. Run `sudo systemctl enable pixel_multiplier.service && sudo systemctl start pixel_multiplier.service`.

## Warnings

There's nothing preventing you from routing input in a circle; please be certain you know what you are doing when configuring `pixel_multiplier.conf`. Because I wrote this utility for my own use, it is presented here only as a courtesy. I have not exhaustively tested it. Also, if you look at my code, you'll see I am a beginner. I'm sure there are better ways to do what I'm doing here. You're welcome to pitch in and help if you can.