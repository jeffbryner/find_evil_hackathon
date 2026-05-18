# Dissect
The dissect series of utilities are handy sniper forensics tools that allow you quickly retrieve an analyze adhoc artifacts from forensic disk images. (Not for memory images)

## Overview
The tools are broken down into `target-<utility>` command line interfaces as follows: 

- target-info: General information
- target-query: General queries across a variety of operating system artifacts.
- target-req: Windows registry utilities

## General Use

- `uv run target-query`
- `-q` option to quiet extraneous stdout
- `-s` to force string/ascii only output (converts from the `records` format to string)
```shell
uv run target-query <forensic_disk_image_filename> -f <plugin> -qs
```
##Examples

Basic information about an image: 
```shell
uv run target-info -q <forensic_disk_image_filename>

Mounts
- <Mount fs='virtual' path='c:'>
- <Mount fs='virtual' path='sysvol'>

Hostname       : <something>
Domain         : <some>.lan
Ips            : 172.16.6.12, 10.10.150.180
Os family      : windows
Os version     : Windows 10 Enterprise (NT 10.0) 16299.611
Architecture   : amd64-win64
Language       : en_US
Timezone       : America/New_York
Install date   : 2018-05-07T19:25:35.000000+00:00
Last activity  : 2018-09-07T22:33:31.440089+00:00
```

## Retrieve runkeys
```shell
uv run target-query <forensic_disk_image_filename> -f runkeys
<windows/registry/run hostname='SOME-THING-02' domain='SOME.lan' ts=2018-06-01 02:42:20.818747+00:00 name='SecurityHealth' command=(executable='%ProgramFiles%\Windows', args=['Defender\\MSASCuiL.exe']) key='HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run' regf_hive_path='sysvol/windows/system32/config/SOFTWARE' regf_key_path='Microsoft\\Windows\\CurrentVersion\\Run' username=None user_id=None user_group=None user_home=None>
```

## Powershell history
```shell
uv run target-query <forensic_disk_image> -f powershell_history -qs

<powershell/history hostname='SOME-02' domain='SOME.lan' mtime=2018-08-31 00:43:21.332932+00:00 order=0 command="<something>')" source='C:\<some>\ConsoleHost_history.txt' username='<some>' user_id='S-1-5-21-3445421715-2530590580-...-1193' user_group=None user_home='C:\\Users\\<some>'>
```

# Windows Registry Details
- `target-reg` will allow you to query a registry hive/key
- `-k` the registry key name
- `-d` for the depth level of traversal

```shell
uv run target-reg <forensic_disk_image_filename> -k "HKEY_LOCAL_MACHINE" -d 2 -q
+ 'HKEY_LOCAL_MACHINE' (None)
  + 'SAM' (2016-11-21 01:56:47.344309+00:00)
    + 'SAM' (2018-05-04 18:14:46.474447+00:00)
      - 'C' b"\x08\x00\x01\x00\x00\x00\x00\x00\xd0\x00\x00\x00\x03\x00\x01\x00\x01\x00\x14\x80\xb0\x00\x00\x00\x...
      - 'ServerDomainUpdates' b'\xfe\xff\x03'
...
```

Key paths with slashes are escaped:

```shell
uv run target-reg b<forensic_disk_image_filename> -k "HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" -d 2 -q
+ 'Run' (2018-06-01 02:42:20.818747+00:00)
  - 'SecurityHealth' '%ProgramFiles%\\Windows Defender\\MSASCuiL.exe'
  - 'VMware User Process' '"C:\\Program Files\\VMware\\VMware Tools\\vmtoolsd.exe" -n vmusr'
```


## Filtering output with rdump
`rdump` is used to process, filter and format target-query results. By default, target-query generates records. Records in this sense are binary representations of parsed artefacts. They are transformed to text by the default mechanism. An example is given below:

```xml
<record key1="value1" key2="value2" >
```
With `rdump` you can transform the stream of records to your liking. The `rdump` utility allows you to:

- Select certain fields from the records.
- Filter certain records. 
- Create additional derived fields.
- Limit the output.
- Format the results.
- Write the results through an adapter.

### Selecting fields / Filtering
Filtering records can be done through the -s option. The selection option must be a Python-expression, where the record is represented with the symbol r. 

An example to query users and eliminate all records that, for example, have no domain value:

```shell
uv run target-query host.img -f users | uv run rdump -F name,home -s "r.domain is not None"
```

Transform to JSONLINE output with -J
```shell 
uv run target-query host.img -f users | uv run rdump -J
```



## All plugins: 
A full list of available plugin modules for `target-query` with the `-l` option: 

```shell
uv run target-query -l

Available plugins:
    apps:
      av:
        mcafee:
          mcafee.msc - Return msc log history records from McAfee. (output: records)
        sophos:
          sophos.hitmanlogs - Return alert log records from Sophos Hitman Pro/Alert. (output: records)
          sophos.sophoshomelogs - Return log history records from Sophos Home. (output: records)
        symantec:
          symantec.firewall - Return log firewall records. (output: records)
          symantec.logs - Return log records. (output: records)
        trendmicro:
          trendmicro.wffirewall - Return Trend Micro Worry-free firewall log history records. (output: records)
          trendmicro.wflogs - Return Trend Micro Worry-free log history records. (output: records)
      browser:
        brave:
          brave.cookies - Return browser cookie records for Brave. (output: records)
          brave.downloads - Return browser download records for Brave. (output: records)
          brave.extensions - Return browser extension records for Brave. (output: records)
          brave.history - Return browser history records for Brave. (output: records)
          brave.passwords - Return browser password records for Brave. (output: records)
        browser:
          browser.cookies - Return cookies for: chromium, edge, firefox, brave, chrome (output: records)
          browser.downloads - Return downloads for: chromium, edge, iexplore, firefox, brave, chrome (output: records)
          browser.extensions - Return extensions for: chromium, edge, firefox, brave, chrome (output: records)
          browser.history - Return history for: chromium, edge, iexplore, firefox, brave, chrome, safari (output: records)
          browser.passwords - Return passwords for: chromium, edge, firefox, brave, chrome (output: records)
        chrome:
          chrome.cookies - Return browser cookie records for Google Chrome. (output: records)
          chrome.downloads - Return browser download records for Google Chrome. (output: records)
          chrome.extensions - Return browser extension records for Google Chrome. (output: records)
          chrome.history - Return browser history records for Google Chrome. (output: records)
          chrome.passwords - Return browser password records for Google Chrome. (output: records)
        chromium:
          chromium.cookies - Return browser cookie records for Chromium browser. (output: records)
          chromium.downloads - Return browser download records for Chromium browser. (output: records)
          chromium.extensions - Return browser extension records for Chromium browser. (output: records)
          chromium.history - Return browser history records for Chromium browser. (output: records)
          chromium.passwords - Return browser password records for Chromium browser. (output: records)
        edge:
          edge.cookies - Return browser cookie records for Microsoft Edge. (output: records)
          edge.downloads - Return browser download records for Microsoft Edge. (output: records)
          edge.extensions - Return browser extension records for Microsoft Edge. (output: records)
          edge.history - Return browser history records for Microsoft Edge. (output: records)
          edge.passwords - Return browser password records for Microsoft Edge. (output: records)
        firefox:
          firefox.cookies - Return browser cookie records from Firefox. (output: records)
          firefox.downloads - Return browser download records from Firefox. (output: records)
          firefox.extensions - Return browser extension records for Firefox. (output: records)
          firefox.history - Return browser history records from Firefox. (output: records)
          firefox.passwords - Return Firefox browser password records. (output: records)
        iexplore:
          iexplore.downloads - Return browser downloads records from Internet Explorer. (output: records)
          iexplore.history - Return browser history records from Internet Explorer. (output: records)
        safari:
          safari.history - Return browser history records from Safari. (output: records)
      chat:
        chat:
          chat.history - Return history for: msn (output: records)
        msn:
          msn.history - Yield MSN chat history messages. (output: records)
      container:
        container:
          container.containers - Return containers for: docker, podman (output: records)
          container.images - Return images for: docker, podman (output: records)
          container.logs - Return logs for: docker, podman (output: records)
        docker:
          docker.containers - Returns any docker containers present on the target system. (output: records)
          docker.images - Returns any pulled docker images on the target system. (output: records)
          docker.logs - Returns log files (stdout/stderr) from Docker containers. (output: records)
        podman:
          podman.containers - Yield any Podman containers on the target system. (output: records)
          podman.images - Yield any pulled Podman images on the target system. (output: records)
          podman.logs - Returns log files (stdout/stderr) from Podman containers. (output: records)
      editor:
        editor:
          editor.extensions - Yields installed extensions. (output: text)
          editor.history - Yields history of files. (output: text)
          editor.tabs - Return tabs for: windowsnotepad (output: records)
        windowsnotepad:
          editor.extensions - Yields installed extensions. (output: text)
          windowsnotepad.history - Return contents from Windows 11 Notepad tabs - and its deleted content if available. (output: records)
          windowsnotepad.tabs - Return contents from Windows 11 Notepad tabs - and its deleted content if available. (output: records)
      edr:
        acquire:
          acquire.handles - Return open handles collected by Acquire. (output: records)
          acquire.hashes - Return file hashes collected by Acquire. (output: records)
        velociraptor:
          velociraptor.results - Return Rapid7 Velociraptor artifacts. (output: records)
      other:
        env:
          envfile - Yield environment variables found in ``.env`` files at the provided path. (output: records)
      productivity:
        msoffice:
          msoffice.native - Returns all native (COM / VSTO) add-ins by parsing the registry and manifest files. (output: records)
          msoffice.startup - Returns all startup items found in Microsoft Office startup folders. (output: records)
          msoffice.web - Returns all available Web add-ins cached in the WEF (Web Extension Framework) folder. (output: records)
        sevenzip:
          7zip - Return 7-Zip GUI history information from the registry. (output: records)
          sevenzip - Return 7-Zip GUI history information from the registry. (output: records)
        winrar:
          winrar - Return all available WinRAR history registry key values. (output: records)
      remoteaccess:
        anydesk:
          anydesk.filetransfer - Parse AnyDesk filetransfer files. (output: records)
          anydesk.logs - Parse AnyDesk trace files. (output: records)
        remoteaccess:
          remoteaccess.filetransfer - Return filetransfer for: anydesk, splashtop (output: records)
          remoteaccess.incoming - Return incoming for: teamviewer (output: records)
          remoteaccess.logs - Return logs for: anydesk, rustdesk, splashtop, teamviewer (output: records)
        rustdesk:
          rustdesk.logs - Parse RustDesk log files. (output: records)
        splashtop:
          splashtop.filetransfer - Parse Splashtop filetransfers. (output: records)
          splashtop.logs - Parse Splashtop log files. (output: records)
        teamviewer:
          teamviewer.incoming - Yield TeamViewer incoming connection logs. (output: records)
          teamviewer.logs - Yield TeamViewer client logs. (output: records)
      shell:
        powershell:
          powershell_history - Return PowerShell command history for all users. (output: records)
        wget:
          wget.hsts - Yield domain entries found in wget HSTS files. (output: records)
      ssh:
        openssh:
          openssh.authorized_keys - Yields the content of the authorized_keys files on a target for each user. (output: records)
          openssh.known_hosts - Yields the content of the known_hosts files on a target for each user. (output: records)
          openssh.private_keys - Yields OpenSSH private keys on a target for each user. (output: records)
          openssh.public_keys - Yields all OpenSSH public keys from all user home directories and the OpenSSH daemon directory. (output: records)
        opensshd:
          opensshd.config - Parse all fields in the SSH server config in /etc/ssh/sshd_config. (output: records)
        putty:
          putty.known_hosts - Parse PuTTY saved SshHostKeys. (output: records)
          putty.sessions - Parse PuTTY saved session configuration files. (output: records)
        ssh:
          ssh.authorized_keys - Return authorized_keys for: openssh (output: records)
          ssh.config - Return config for: opensshd (output: records)
          ssh.known_hosts - Return known_hosts for: openssh, putty (output: records)
          ssh.private_keys - Return private_keys for: openssh (output: records)
          ssh.public_keys - Return public_keys for: openssh (output: records)
          ssh.sessions - Return sessions for: putty (output: records)
      virtualization:
        vmware_workstation:
          vmware.clipboard - Yield cached VMware Workstation drag-and-drop file artifacts. (output: records)
          vmware.config - Yield VMware Workstation Virtual Machine inventory configurations. (output: records)
          vmware.draganddrop - Yield cached VMware Workstation drag-and-drop file artifacts. (output: records)
      vpn:
        openvpn:
          openvpn.config - Parses config files from openvpn interfaces. (output: records)
        wireguard:
          wireguard.config - Parses interface config files from wireguard installations. (output: records)
      webhosting:
        cpanel:
          cpanel.lastlogin - Return the content of the cPanel lastlogin file. (output: records)
      webserver:
        apache:
          apache.access - Return contents of Apache access log files in unified ``WebserverAccessLogRecord`` format. (output: records)
          apache.certificates - Return host certificates for found Apache ``VirtualHost`` directives. (output: records)
          apache.error - Return contents of Apache error log files in unified ``WebserverErrorLogRecord`` format. (output: records)
          apache.hosts - Return found ``VirtualHost`` directives in the Apache configuration. (output: records)
          webserver.logs - Returns log file records from installed webservers. (output: records)
        caddy:
          caddy.access - Parses Caddy V1 CRF and Caddy V2 JSON access logs. (output: records)
          webserver.logs - Returns log file records from installed webservers. (output: records)
        citrix:
          apache.access - Return contents of Apache access log files in unified ``WebserverAccessLogRecord`` format. (output: records)
          apache.certificates - Return host certificates for found Apache ``VirtualHost`` directives. (output: records)
          apache.error - Return contents of Apache error log files in unified ``WebserverErrorLogRecord`` format. (output: records)
          apache.hosts - Return found ``VirtualHost`` directives in the Apache configuration. (output: records)
          webserver.logs - Returns log file records from installed webservers. (output: records)
        iis:
          iis.access - Return contents of IIS (v7 and above) log files in unified WebserverAccessLogRecord format. (output: records)
          iis.logs - Return contents of IIS (v7 and above) log files. (output: records)
        nginx:
          nginx.access - Return contents of NGINX access log files in unified ``WebserverAccessLogRecord`` format. (output: records)
          nginx.certificates - Return found server certificates in the NGINX configuration. (output: records)
          nginx.error - Return contents of NGINX error log files in unified ``WebserverErrorLogRecord`` format. (output: records)
          nginx.hosts - Return found server directives in the NGINX configuration. (output: records)
          webserver.logs - Returns log file records from installed webservers. (output: records)
        webserver:
          webserver.access - Return access for: iis, apache, nginx, caddy, citrix (output: records)
          webserver.certificates - Return certificates for: apache, nginx, citrix (output: records)
          webserver.error - Return error for: apache, nginx, citrix (output: records)
          webserver.hosts - Return hosts for: apache, nginx, citrix (output: records)
          webserver.logs - Returns log file records from installed webservers. (output: records)
    filesystem:
      icat:
        icat - Output the contents of a file based on its MFT segment or inode number. Supports Alternate Data Streams (output: no output)
      ntfs:
        mft:
          mft.body - Return the MFT records of all NTFS filesystems in bodyfile format. (output: lines)
          mft.records - Return the MFT records of all NTFS filesystems. (output: records)
          mft.timeline - Return the MFT records of all NTFS filesystems in a human readable format (unsorted). (output: lines)
        mft_timeline:
          mft_timeline - Return the MFT records of all NTFS filesystems in a human readable format (unsorted) (deprecated, use mft.timeline). (output: lines)
        usnjrnl:
          usnjrnl - Return the UsnJrnl entries of all NTFS filesystems. (output: records)
      unix:
        capability:
          capability_binaries - Find all files that have capabilities set on files. (output: records)
        suid:
          suid_binaries - Return all SUID binaries. (output: records)
      walkfs:
        walkfs - Walk a target's filesystem and return all filesystem entries. (output: records)
      yara:
        yara - Scan files inside the target up to a given maximum size with YARA rule file(s). (output: records)
    general:
      example:
        example_namespace.example_record - Example namespace export. (output: records)
        example - Example plugin function. (output: text)
        example_none - Example plugin with no return value. (output: no output)
        example_record - Example plugin that generates records. (output: records)
        example_user_registry_record - Example plugin that generates records with registry key and user information. (output: records)
        example_yield - Example plugin that yields text lines. (output: lines)
      loaders:
        loaders - List the available loaders. (output: no output)
      osinfo:
        osinfo - Yield grouped records with target OS info. (output: records)
      plugins:
        plugins - Print all available plugins. (output: no output)
    os:
      default:
        _os:
          architecture - Return a slug of the target's OS architecture. (output: text)
          hostname - Return the target's hostname. (output: text)
          ips - Return the IP addresses configured in the target. (output: text)
          os - Return a slug of the target's OS name. (output: text)
          users - Return the users available in the target. (output: records)
          version - Return the target's OS version. (output: text)
        locale:
          keyboard - Get the keyboard layout(s) of the system. (output: records)
          language - Get the configured locale(s) of the system. (output: text)
          timezone - Get the timezone of the system. (output: text)
        network:
          network.dns - Return DNS addresses as list of :class:`str`. (output: text)
          network.gateways - Return gateways as list of :class:`IPAddress`. (output: text)
          network.interfaces - Yield interfaces. (output: records)
          network.ips - Return IP addresses as list of :class:`IPAddress`. (output: text)
          network.macs - Return MAC addresses as list of :class:`str`. (output: text)
      unix:
        applications:
          applications - Yield installed Unix GUI applications from GNOME and XFCE. (output: records)
        bsd:
          citrix:
            generic:
              install_date - Return the likely install date of Citrix Netscaler. (output: text)
            history:
              bashhistory - Return shell history for all UNIX users. (output: records)
              commandhistory - Return shell history for all Citrix users. (output: records)
            locale:
              keyboard - Get the keyboard layout(s) of the system. (output: records)
              language - Return configured UI language(s). (output: text)
              timezone - Return configured timezone. (output: text)
          darwin:
            ios:
              applications:
                applications - Yield installed iOS apps. (output: records)
              generic:
                activity - Return last seen activity based on filesystem timestamps. (output: text)
                install_date - Return the likely install date of the operating system. (output: text)
              locale:
                language - Return the configured language(s) of the iOS system. (output: text)
                timezone - Return the configured localtime of the iOS system. (output: text)
            macos:
              network:
                network.dns - Return DNS addresses as list of :class:`str`. (output: text)
                network.gateways - Return gateways as list of :class:`IPAddress`. (output: text)
                network.interfaces - Yield interfaces. (output: records)
                network.ips - Return IP addresses as list of :class:`IPAddress`. (output: text)
                network.macs - Return MAC addresses as list of :class:`str`. (output: text)
              user:
                account_policy - Yield user account policy information. (output: records)
        cronjobs:
          cronjobs - Yield cronjobs, and their configured environment variables on a Unix system (output: records)
        esxi:
          vm:
            vm.inventory - Yield all virtual machines registered on the ESXi host. (output: records)
            vm.orphaned - Yield all virtual machines found at ``/vmfs/volumes/*/*/*.vmx`` that are NOT in the inventory. (output: records)
        etc:
          etc:
            etc.etc - This plugin yields configuration information from the etc directory in key value pairs. (output: records)
        generic:
          activity - Return last seen activity based on filesystem timestamps. (output: text)
          install_date - Return the likely install date of the operating system. (output: text)
        history:
          bashhistory - Return shell history for all UNIX users. (output: records)
          commandhistory - Return shell history for all UNIX users. (output: records)
        linux:
          cmdline:
            cmdline - Return the complete command line for all processes. (output: records)
          debian:
            apt:
              apt.logs - Package manager log parser for Apt. (output: records)
            dpkg:
              dpkg.log - Yield records for actions logged in dpkg's logs. (output: records)
              dpkg.status - Yield records for packages in dpkg's status database. (output: records)
            proxmox:
              vm:
                vmlist - List Proxmox virtual machines on this node. (output: records)
            snap:
              snap - Yields installed Canonical Linux Snapcraft (snaps) applications on the target system. (output: records)
              snaps - Yields installed Canonical Linux Snapcraft (snaps) applications on the target system. (output: records)
          environ:
            environ - Return the initial environment for all processes when they were started via execve(2). (output: records)
          fortios:
            generic:
              activity - Return last seen activity based on filesystem timestamps. (output: text)
              install_date - Return the likely install date of FortiOS. (output: text)
            locale:
              keyboard - Get the keyboard layout(s) of the system. (output: records)
              language - Return configured UI language. (output: text)
              timezone - Return configured UI/system timezone. (output: text)
          iptables:
            iptables - Return iptables and ufw rules saved using iptables-save. (output: records)
          modules:
            lsmod - Return information about active kernel modules in lsmod format. (output: lines)
            sysmodules - Return information about active kernel modules. (output: records)
          netstat:
            netstat - This plugin mimics the output `netstat -tunelwap` would generate on a Linux machine. (output: lines)
          network:
            network.dhcp - Return interfaces obtained via DHCP. (output: records)
            network.dns - Return DNS addresses as list of :class:`str`. (output: text)
            network.gateways - Return gateways as list of :class:`IPAddress`. (output: text)
            network.interfaces - Yield interfaces. (output: records)
            network.ips - Return IP addresses as list of :class:`IPAddress`. (output: text)
            network.macs - Return MAC addresses as list of :class:`str`. (output: text)
          processes:
            processes - Return the processes available in ``/proc`` and the stats associated with them. (output: records)
          recentlyused:
            recently_used - Parse recently-used.xbel files on Linux Desktops. (output: records)
          redhat:
            yum:
              yum.logs - Package manager log parser for CentOS' Yellowdog Updater (Yum). (output: records)
          services:
            services - Return information about all installed systemd and init.d services. (output: records)
          sockets:
            sockets.packet - This plugin yields the packet sockets and available stats associated with them. (output: records)
            sockets.raw - This plugin yields the raw and raw6 sockets and available stats associated with them. (output: records)
            sockets.tcp - This plugin yields the tcp and tcp6 sockets and available stats associated with them. (output: records)
            sockets.udp - This plugin yields the udp and udp6 sockets and available stats associated with them. (output: records)
            sockets.unix - This plugin yields the unix sockets and available stats associated with them. (output: records)
          suse:
            zypper:
              zypper.logs - Package manager log parser for SuSE's Zypper. (output: records)
        locale:
          keyboard - Get the keyboard layout(s) of the system. (output: records)
          language - Get the configured locale(s) of the system. (output: text)
          timezone - Get the timezone of the system. (output: text)
        locate:
          gnulocate:
            gnulocate.locate - Yield file and directory names from GNU findutils' locatedb file. (output: records)
          locate:
            locate.locate - Return locate for: plocate, gnulocate, mlocate (output: records)
          mlocate:
            mlocate.locate - Yield file and directory names from mlocate.db file. (output: records)
          plocate:
            plocate.locate - Yield file and directory names from the plocate.db. (output: records)
        log:
          atop:
            atop - Return the content of Atop log files. (output: records)
          audit:
            audit - Return CentOS and RedHat audit information stored in /var/log/audit*. (output: records)
          auth:
            authlog - Yield contents of ``/var/log/auth.log*`` and ``/var/log/secure*`` files. (output: records)
            securelog - Yield contents of ``/var/log/auth.log*`` and ``/var/log/secure*`` files. (output: records)
          journal:
            journal - Return the contents of Systemd Journal log files. (output: records)
          lastlog:
            lastlog - Return last logins information from /var/log/lastlog. (output: records)
          messages:
            messages - Return contents of /var/log/messages*, /var/log/syslog* and cloud-init logs. (output: records)
            syslog - Return contents of /var/log/messages*, /var/log/syslog* and cloud-init logs. (output: records)
          utmp:
            btmp - Return failed login attempts stored in the btmp file. (output: records)
            utmp - Yield contents of wtmp log files. (output: records)
            wtmp - Yield contents of wtmp log files. (output: records)
        packagemanager:
          packagemanager.logs - Return logs for: apt, yum, zypper (output: records)
        shadow:
          passwords - Yield shadow records from /etc/shadow files. (output: records)
        trash:
          recyclebin - Yield deleted files from GNOME Trash folders. (output: records)
          trash - Yield deleted files from GNOME Trash folders. (output: records)
      windows:
        activitiescache:
          activitiescache - Return ActivitiesCache.db database content. (output: records)
        ad:
          ntds:
            ad.computers - Extract all computer accounts from the NTDS.dit database. (output: records)
            ad.group_policies - Extract all group policy objects (GPO) NTDS.dit database. (output: records)
            ad.users - Extract all user accounts from the NTDS.dit database. (output: records)
        adpolicy:
          adpolicy - Return all AD policies (also known as GPOs or Group Policy Objects). (output: records)
        amcache:
          amcache.applaunches - Return PcaAppLaunchAppcompatRecord records from Amcache PCA AppLaunch files (Windows 11 22H2 or later). (output: records)
          amcache.application_files - Return InventoryApplicationFile records from Amcache hive. (output: records)
          amcache.applications - Return InventoryApplication records from Amcache hive. (output: records)
          amcache.device_containers - Return InventoryDeviceContainer records from Amcache hive. (output: records)
          amcache.drivers - Return InventoryDriverBinary records from Amcache hive. (output: records)
          amcache.files - Return File records from Amcache hive. (output: records)
          amcache.general - Return PcaGeneralAppcompatRecord records from Amcache PCA General files (Windows 11 22H2 or later). (output: records)
          amcache.programs - Return Programs records from Amcache hive. (output: records)
          amcache.shortcuts - Return InventoryApplicationShortcut records from Amcache hive. (output: records)
        cam:
          cam.history - Iterate Capability Access Manager History entries. (output: records)
          cam.registry - Iterate Capability Access Manager key locations. (output: records)
        catroot:
          catroot.catdb - Return the hash values present in the catdb files in the catroot2 folder. (output: records)
          catroot.files - Return the content of the catalog files in the CatRoot folder. (output: records)
        certlog:
          certlog.certificate_extensions - Return the contents of ``CertificateExtensions`` table from all Certificate Authority databases. (output: records)
          certlog.certificates - Return the contents of ``Certificates`` table from all Certificate Authority databases. (output: records)
          certlog.crls - Return the contents of the ``CRLs`` table from all Certificate Authority databases. (output: records)
          certlog.request_attributes - Return the contents of the ``RequestAttributes`` table from all Certificate Authority databases. (output: records)
          certlog.requests - Return the contents of the ``Requests`` table from all Certificate Authority databases. (output: records)
        cim:
          cim.consumerbindings - Return all ActiveScriptEventConsumer and CommandLineEventConsumer. (output: records)
        clfs:
          clfs - Parse the containers associated with a valid BLF file. (output: records)
        credential:
          credential:
            credential.credhist - Return credhist for: credhist (output: records)
            credential.defaultpassword - Return defaultpassword for: defaultpassword (output: records)
            credential.winlogon - Return winlogon for: winlogon (output: records)
          credhist:
            credhist.credhist - Yield and decrypt all Windows CREDHIST entries on the target. (output: records)
          defaultpassword:
            defaultpassword.defaultpassword - Yield decrypted Windows LSA DefaultPassword records. (output: records)
          winlogon:
            winlogon.winlogon - Yield Windows Winlogon DefaultPassword strings. (output: records)
        defender:
          defender.evtx - Parse Microsoft Defender evtx log files. (output: records)
          defender.exclusions - Yield Microsoft Defender exclusions from the Registry. (output: records)
          defender.mpcmdrun - Return entries in Defender ``MpCmdRun.log`` files from ``MpCmdRun.exe`` invocations. (output: records)
          defender.mplog - Return the contents of the Defender MPLog file. (output: records)
          defender.quarantine - Parse the quarantine folder of Microsoft Defender for quarantine entry resources. (output: records)
          defender.recover - Recover files that have been placed into quarantine by Microsoft Defender. (output: no output)
        dpapi:
          keyprovider:
            credhist:
              dpapi.keyprovider.credhist.keys - Yield Windows CREDHIST SHA1 hashes. (output: lines)
            defaultpassword:
              lsa:
                dpapi.keyprovider.defaultpassword.lsa.keys - Yield Windows LSA DefaultPassword strings. (output: lines)
              winlogon:
                dpapi.keyprovider.defaultpassword.winlogon.keys - Yield Windows Winlogon DefaultPassword strings. (output: lines)
            empty:
              dpapi.keyprovider.empty.keys - Yield an empty string. (output: lines)
            keychain:
              dpapi.keyprovider.keychain.keys - Yield keychain passphrases. (output: lines)
            keyprovider:
              dpapi.keyprovider.keys - Return keys for: dpapi.keyprovider.empty, dpapi.keyprovider.keychain, dpapi.keyprovider.credhist, dpapi.keyprovider.defaultpassword.lsa, dpapi.keyprovider.defaultpassword.winlogon (output: lines)
        env:
          environment_variables - Return all environment variables on a Windows system. (output: records)
          path_extensions - Return all found path extensions. (output: records)
        everything:
          everything.locate - Yield file and directory names from everything.db file. (output: records)
        exchange:
          exchange:
            exchange.transport_agents - Print the content of the config file for Transport Agents for Microsoft Exchange. (output: no output)
        firewall:
          firewall.logs - Parse Windows Firewall log files. (output: records)
          firewall.rules - Return firewall rules saved in the Windows registry. (output: records)
        generic:
          activity - Return last seen activity based on filesystem timestamps. (output: text)
          alternateshell - Return the AlternateShell registry key value. (output: records)
          appinit - Return all available Application Initial (AppInit) DLLs registry key values. (output: records)
          bootshell - Return the BootShell registry key entry. (output: records)
          codepage - Returns the current active codepage on the system. (output: text)
          commandprocautorun - Return all available Command Processor (cmd.exe) AutoRun registry key values. (output: records)
          domain - Return the domain name. (output: text)
          domain_sid - Return the domain SID of the system. (output: records)
          filerenameop - Return all pending file rename operations. (output: records)
          install_date - Returns the install date of the system. (output: text)
          knowndlls - Return all available KnownDLLs registry key values. (output: records)
          machine_sid - Return the machine SID of the system. (output: records)
          ndis - Return network registry key entries. (output: records)
          ntversion - Return the Windows NT version. (output: text)
          nullsessionpipes - Return the NullSessionPipes registry key value. (output: records)
          pathenvironment - Return the content of the Windows PATH environment variable. (output: lines)
          sessionmanager - Return interesting Session Manager (Smss.exe) registry key entries. (output: records)
          sid - Return the machine- and optional domain SID of the system. (output: records)
          winsocknamespaceprovider - Return available protocols stored in the Winsock catalog database. (output: records)
        jumplist:
          jumplist.automatic_destination - Return the content of AutomaticDestination Windows Jump Lists. (output: records)
          jumplist.custom_destination - Return the content of CustomDestination Windows Jump Lists. (output: records)
        lnk:
          lnk - Parse all .lnk files in /ProgramData, /Users, and /Windows or from a specified path in record format. (output: records)
        locale:
          keyboard - Yield records of installed keyboards on the system. (output: records)
          language - Get a list of installed languages on the system. (output: text)
          timezone - Get the configured timezone of the system in IANA TZ standard format. (output: text)
        log:
          agentexecutor:
            agentexecutor - Parse the AgentExecutor.log and yield structured records. (output: records)
          amcache:
            amcache_install - Return the contents of the Amcache install log. (output: records)
          etl:
            etl.boot - Return the contents of the ETL files created at last boot. (output: records)
            etl.etl - Return the contents of the ETL files generated at last boot and last shutdown. (output: records)
            etl.shutdown - Return the contents of the ETL files created at last shutdown. (output: records)
          evt:
            evt - Parse Windows Eventlog files (``*.evt``). (output: records)
            scraped_evt - Yields EVT log file records scraped from target disks. (output: records)
          evtx:
            evtx - Return entries from Windows Event log files (``*.evtx``). (output: records)
            scraped_evtx - Return EVTX log file records scraped from target disks. (output: records)
          intunemanagementextension:
            intunemanagementextension - Parse Intune Management Extension log files. (output: records)
          mssql:
            mssql.errorlog - Return all Microsoft SQL Server ERRORLOG messages. (output: records)
          pfro:
            pfro - Return the content of %windir%/PFRO.log (output: records)
          schedlgu:
            schedlgu - Return all events in the Task Scheduler Service transaction log file (SchedLgU.txt). (output: records)
        lsa:
          lsa.secrets - Yield decrypted LSA secrets from a Windows target. (output: records)
        network:
          network.dns - Return DNS addresses as list of :class:`str`. (output: text)
          network.gateways - Return gateways as list of :class:`IPAddress`. (output: text)
          network.interfaces - Yield interfaces. (output: records)
          network.ips - Return IP addresses as list of :class:`IPAddress`. (output: text)
          network.macs - Return MAC addresses as list of :class:`str`. (output: text)
        notifications:
          notifications.appdb - Retrun the data from Windows appdb.dat file. (output: records)
          notifications.wpndatabase - Returns Windows Notifications from wpndatabase.db (post Windows 10 Anniversary). (output: records)
        prefetch:
          prefetch - Return the content of all prefetch files. (output: records)
        productkey:
          license - Yield Windows product key(s) of the target. (output: records)
          productkey - Yield Windows product key(s) of the target. (output: records)
        rdpcache:
          rdpcache.paths - Yield paths and timestamps of RDP Cache bitmap files. (output: records)
          rdpcache.recover - Extract bitmaps from Windows' RDP Client cache files. (output: no output)
        recyclebin:
          recyclebin - Return files located in the recycle bin ($Recycle.Bin). (output: records)
        regf:
          applications:
            applications - Yields currently installed applications from the Windows registry. (output: records)
          appxdebugkeys:
            appxdebugkeys - Iterate various AppX debug key locations. See source for all locations. (output: records)
          auditpol:
            auditpol - Return audit policy settings from the registry. (output: records)
          bam:
            bam - Parse bam and dam registry keys. (output: records)
          cit:
            cit.cit - Return CIT data from the registry for executed executable information. (output: records)
            cit.dp - Parse CIT DP data from the registry. (output: records)
            cit.modules - Parse CIT tracked module information from the registry. (output: records)
            cit.puu - Parse CIT PUU (Post Update Usage) data from the registry. (output: records)
            cit.telemetry - Parse CIT process telemetry answers from the registry. (output: records)
          clsid:
            clsid.machine - Return only the machine CLSID registry keys. (output: records)
            clsid.user - Return only the user CLSID registry keys. (output: records)
          mru:
            mru.acmru - Return the ACMru (Windows Search) data. (output: records)
            mru.lastvisited - Return the LastVisitedMRU data. (output: records)
            mru.msoffice - Return MS Office MRU keys. (output: records)
            mru.mstsc - Return Terminal Server Client MRU data. (output: records)
            mru.networkdrive - Return MRU of mapped network drives. (output: records)
            mru.opensave - Return the OpenSaveMRU data. (output: records)
            mru.recentdocs - Return the RecentDocs data. (output: records)
            mru.run - Return the RunMRU data. (output: records)
          muicache:
            muicache - Iterate various MUIcache key locations. (output: records)
          nethist:
            network_history - Return attached network history. (output: records)
          recentfilecache:
            recentfilecache - Parse RecentFileCache.bcf. (output: records)
          regf:
            regf - Return all registry keys and values. (output: records)
          runkeys:
            runkeys - Iterate various run key locations. See source for all locations. (output: records)
          shellbags:
            shellbags - Yields Windows Shellbags. (output: records)
          shimcache:
            shimcache - Return the shimcache. (output: records)
          trusteddocs:
            trusteddocs - Return Microsoft Office TrustRecords registry keys for all Office applications. (output: records)
          usb:
            usb - Yields information about (historically) attached USB storage devices on Windows. (output: records)
          userassist:
            userassist - Return the UserAssist information for each user. (output: records)
        sam:
          sam - Dump SAM entries (output: records)
        search:
          search - Yield Windows Search Index records. (output: records)
        services:
          services - Return information about all installed Windows services. (output: records)
        sru:
          sru.application - Return the contents of Application Resource Usage table from the SRUDB.dat file. (output: records)
          sru.application_timeline - Return the contents of App Timeline Provider table from the SRUDB.dat file. (output: records)
          sru.energy_estimator - Return the contents of Energy Estimator table from the SRUDB.dat file. (output: records)
          sru.energy_usage - Return the contents of Energy Usage Provider table from the SRUDB.dat file. (output: records)
          sru.energy_usage_lt - Return the contents of Energy Usage Provider Long Term table from the SRUDB.dat file. (output: records)
          sru.network_connectivity - Return the contents of Windows Network Connectivity Usage Monitor table from the SRUDB.dat file. (output: records)
          sru.network_data - Return the contents of Windows Network Data Usage Monitor table from the SRUDB.dat file. (output: records)
          sru.push_notification - Return the contents of Windows Push Notification Data table from the SRUDB.dat file. (output: records)
          sru.sdp_cpu_provider - Return the contents of SDP CPU Provider table from the SRUDB.dat file. (output: records)
          sru.sdp_network_provider - Return the contents of SDP Network Provider table from the SRUDB.dat file. (output: records)
          sru.sdp_physical_disk_provider - Return the contents of SDP Physical Disk Provider table from the SRUDB.dat file. (output: records)
          sru.sdp_volume_provider - Return the contents of SDP Volume Provider table from the SRUDB.dat file. (output: records)
          sru.vfu - Return the contents of vfuprov table from the SRUDB.dat file. (output: records)
        startupinfo:
          startupinfo - Return the contents of StartupInfo files. (output: records)
        syscache:
          syscache - Parse the objects in the ObjectTable from the Syscache.hve file. (output: records)
        tasks:
          tasks - Return all scheduled tasks on a Windows system. (output: records)
        thumbcache:
          thumbcache.iconcache - Yield iconcache thumbnails. (output: records)
          thumbcache.thumbcache - Yield thumbcache thumbnails. (output: records)
        ual:
          ual.client_access - Return client access data within the User Access Logs. (output: records)
          ual.domains_seen - Return DNS data within the User Access Logs. (output: records)
          ual.role_access - Return role access data within the User Access Logs. (output: records)
          ual.system_identities - Return system identity data within the User Access Logs. (output: records)
          ual.virtual_machines - Return virtual machine data within the User Access Logs. (output: records)
        wer:
          wer - Return information from Windows Error Reporting (WER) files. (output: records)
        wua_history:
          wua_history - Returns all available historical Windows Update Agent operations stored in the DataStore.edb. (output: records)
    scrape:
      qfind:
        qfind - Find a needle in a haystack. (output: records)

Failed to load:
    None

Available loaders:
    ab - Load Android backup files.
    ad1 - Access Data ``.ad`` loader.
    asdf - Load an ASDF target.
    cb - Use Carbon Black endpoints as targets using Live Response.
    cellebrite - Load Cellebrite UFED exports (``.ufdx`` and ``.ufd``).
    cyber - No documentation.
    dir - Load a directory as a filesystem.
    hyperv - Load Microsoft Hyper-V hypervisor files.
    itunes - Load iTunes backup files.
    kape - Load KAPE forensic image format files.
    libvirt - Load libvirt xml configuration files.
    local - Load local filesystem.
    log - Load separate log files without a target.
    mqtt - Load remote targets through a broker.
    multiraw - Load multiple raw containers as a single target (i.e. a multi-disk system).
    ova - Load Open Virtual Appliance (OVA) files.
    overlay - Load Podman OCI overlay filesystems.
    overlay2 - Load Docker overlay2 filesystems.
    ovf - Load Open Virtualization Format (OVF) files.
    phobos - Load Phobos Ransomware files.
    proxmox - Loader for Proxmox VM configuration files.
    pvm - Parallels VM directory (.pvm).
    pvs - Parallels VM configuration file (config.pvs).
    raw - Load raw container files such as disk images.
    remote - Load a remote target that runs a compatible Dissect agent.
    smb - Use remote SMB servers as targets.
    tanium - Load Tanium forensic image format files.
    tar - Load tar files.
    target - Load target files.
    uac - Loader for extracted UAC collections.
    utm - Load UTM virtual machine files.
    vb - No documentation.
    vbk - Load Veaam Backup (VBK) files.
    vbox - Load Oracle VirtualBox files.
    velociraptor - Load Rapid7 Velociraptor forensic image files.
    vma - Load Proxmox Virtual Machine Archive (VMA) files.
    vmsupport - Loader for extracted ESXi vm-support.
    vmwarevm - Load ``*.vmwarevm`` folders from VMware Fusion.
    vmx - Load VMware virtual machine configuration (VMX) files.
    xva - Load Citrix Hypervisor XVA format files.
    zip - Load zip files.
```
