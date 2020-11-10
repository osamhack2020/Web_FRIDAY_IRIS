[contributors-shield]: https://img.shields.io/github/contributors/osamhack2020/Web_FRIDAY_IRIS?style=flat-square
[contributors-url]: https://github.com/osamhack2020/Web_FRIDAY_IRIS/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/osamhack2020/Web_FRIDAY_IRIS.svg?style=flat-square
[forks-url]: https://github.com/osamhack2020/Web_FRIDAY_IRIS/network/members
[stars-shield]: https://img.shields.io/github/stars/osamhack2020/Web_FRIDAY_IRIS?style=flat-square
[stars-url]: https://github.com/osamhack2020/Web_FRIDAY_IRIS/stargazers
[issues-shield]: https://img.shields.io/github/issues/osamhack2020/Web_FRIDAY_IRIS.svg?style=flat-square
[issues-url]: hhttps://github.com/osamhack2020/Web_FRIDAY_IRIS/issues
[license-shield]: https://img.shields.io/github/license/osamhack2020/Web_FRIDAY_IRIS.svg?style=flat-square
[license-url]: https://github.com/osamhack2020/Web_FRIDAY_IRIS/blob/main/LICENSE

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Apache 2.0 License][license-shield]][license-url]

<h1 align="center"> I R I S </h1>
<p align="center">
  <img src="https://github.com/osamhack2020/Web_FRIDAY_IRIS/blob/main/team_logo.png" width="200" alt="team logo">
</p>

## Prolog

[![Food Waste Disposal Costs Problem](https://img.youtube.com/vi/nciqfJ8wz0g/0.jpg)](https://www.youtube.com/watch?v=nciqfJ8wz0g)

There is vicious circle at cafeteria

Overordering -> Over-food production -> A lot of leftover -> Excessive Food Waste Disposal Costs

The number of people who eat dinner on weekends is greatly reduced, while food production remains unchanged.

This leads to a lot of leftovers.

However, the chef cooked according to the number of people scheduled for the official dinner.

To solve this problem, let's find out how many people are actually going to eat dinner using DeepLearning.

Predictions will be effective if only certain patterns are found in cafeteria

This program consists of several  services that interact each other

## Functional Design

### Database
![HA-Database-Infra](https://drive.google.com/uc?export=download&id=1C9Wra6ZUjt2nFJY5dSKY6zYqQoIZ_dBM)

### [WEB] Attendance Check using QR
[API docs](https://duckhoim.gitbook.io/friday/)

## Prerequisites

* Docker Engine version >= 19.03
* Docker Compose version >= 1.27.4

1. Install docker follow below posts depends on your os

- ["Install Docker at ubuntu 20.04"](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04)
- ["Install Docker at Windows 10"](https://www.wsgvet.com/ubuntu/180?sfl=wr_subject%7C%7Cwr_content&stx=NAS&sst=wr_hit&sod=desc&sop=and&page=1)

2. Docker Compose Installation (Don't need at already installed)

```bash
$ cd scripts
$ ./install_docker-compse.sh
```

### attendance_check service

* Support HTML5 MediaDevices API
  * https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices

## Technique Used

### front-end

 0. common 
 -  Flask
 -  SQLAlchemy

 1. attendance_check
 - [JsQRScanner](https://github.com/jbialobr/JsQRScanner) : qr scanner on website

### Database

 - Mysql ( >= 8.0)

### Load balancer

 - HA Proxy
 - Read / Write Splitting : Before query switch uri that binds SQLAlchemy Object
   - with [adhorn's script](https://gist.github.com/adhorn/b84dc47175259992d406) 

## Installation Process

1-1. Compose Database ( at INFRA_FRIDAY )

IF you use wsl or codespace, checkout branch to wsl or codespace

```bash
$ cd database
$ docker-compose up -d --build
```

1-2. Compose Database ( at Web_FRIDAY )

```bash
$ cd scripts
$ ./run_infra.sh
```

2. Run Attendance Check app ( at Web_FRIDAY )

```bash
$ cd attendance_check
$ docker-compose up -d --build
```

## Getting Started

### attendance_check
> Check the actual number of people who ate.

First, We need to give them a QR Code that include there id

and then bring device that has camera and follow below steps

This service auto check time on device, so you have to check the device time is correct

![qr_scanned_screen](/res/screenshot/check_screen.jpg?raw=true)

1. go to Endpoint ( ```url/qr/scan```) at Web Browser

2. Show QR at rear camera

3. wait 5~10 sec, check your id on screen

## Team Information

- Pyo Sehun (kimpyo9357@naver.com), Github Id: kimpyo9357
- Jeong Deokho (duckhoim@naver.com), Github Id: l0vey0u

## Copyleft / End User License

### License

This software is licensed under the [Apache 2 license](LICENSE), quoted below.

Copyright 2020. Team IRIS

Licensed under the Apache License, Version 2.0 (the "License"); you may not
use this project except in compliance with the License. You may obtain a copy
of the License at http://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations under
the License.

---

JsQRScanner

https://github.com/jbialobr/JsQRScanner

Apache License 2.0
