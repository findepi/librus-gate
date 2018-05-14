# librus-gate

RSS gateway for Synergia Librus's announcements

## Usage

For your convenience, the application comes pre-packaged with all dependencies
as a docker container, [`findepi/librus-gate`](https://hub.docker.com/r/findepi/librus-gate/).

### localhost

1. ```bash
   docker run -d --restart unless-stopped -p 127.0.0.1:8723:8723 --name librus-gate findepi/librus-gate
   ```
   or, if doing this second+ time:
   ```bash
   docker pull findepi/librus-gate &&
   { docker rm -f librus-gate || true; } &&
   docker run -d --restart unless-stopped -p 127.0.0.1:8723:8723 --name librus-gate findepi/librus-gate
   ```
2. Subscribe `http://12345u:p4ssw0rD@127.0.0.1:8723/announcements` in your favorite,
   old-school, desktop-based RSS reader like [Thunderbird](https://www.thunderbird.net/)

Of course, you are not limited to localhost.  I am just too old-school.
