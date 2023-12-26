# TODO:
# - PLDify SysV init scripts
# - drop ibverbs.pc and rdmacm.pc when not used by other packages
#
# Conditional build:
%bcond_without	static_libs	# static libraries
%bcond_without	systemd		# systemd

Summary:	RDMA Core Userspace Libraries and Daemons
Summary(pl.UTF-8):	RDMA Core - biblioteki i demony przestrzeni użytkownika
Name:		rdma-core
Version:	48.0
Release:	1
License:	BSD or GPL v2
Group:		Applications/System
#Source0Download: https://github.com/linux-rdma/rdma-core/releases
Source0:	https://github.com/linux-rdma/rdma-core/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f8901665b2fbf03b4ffb6bf7f6207ac4
Source1:	libibverbs.pc.in
Source2:	librdmacm.pc.in
Patch0:		%{name}-static.patch
# restore cxgb3 and nes providers from rdma-core 26.1 (keep until dropping support for kernels < 5.5)
# from https://github.com/linux-rdma/rdma-core/commit/c21a3cf5d9e4cef0904b4d47f1cb43be9efdbf90.patch cut down (to revert)
Patch1:		%{name}-kernel-abi.patch
# https://github.com/linux-rdma/rdma-core/commit/4daf5c91c1296683924cb9668c3d879da072756b.patch cut down (to revert)
Patch2:		%{name}-nes.patch
# https://github.com/linux-rdma/rdma-core/commit/36588f5844af4ef1e5b0d6ad002fa1adf9032653.patch cut down (to revert)
Patch3:		%{name}-cxgb3.patch
Patch4:		%{name}-providers-update.patch
URL:		https://github.com/linux-rdma/rdma-core
BuildRequires:	cmake >= 2.8.12
BuildRequires:	docutils
# i915_drm.h, amdgpu_drm.h
BuildRequires:	libdrm-devel
BuildRequires:	libnl-devel >= 3.2
# <rdma/*> kernel interface
BuildRequires:	linux-libc-headers >= 7:2.6.20
# if no buildlib/pandoc-prebuilt dir
#BuildRequires:	pandoc
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3
%if %{with python}
BuildRequires:	python3-Cython
BuildRequires:	python3-devel >= 1:3.2
%endif
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	udev-devel
%{?with_systemd:BuildRequires:	systemd-devel}
Requires:	ibacm = %{version}-%{release}
Requires:	iwpmd = %{version}-%{release}
Requires:	rdma-boot = %{version}-%{release}
Requires:	rdma-ndd = %{version}-%{release}
Requires:	srptools = %{version}-%{release}
Requires:	systemd-units
Requires:	udev-core
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ibv_abi		rdmav34

%description
This is the userspace components for the Linux Kernel's
drivers/infiniband subsystem. Specifically this contains the userspace
libraries for the following device nodes:
 - /dev/infiniband/uverbsX (libibverbs)
 - /dev/infiniband/rdma_cm (librdmacm)
 - /dev/infiniband/umadX (libibumad)

The userspace component of the libibverbs RDMA kernel drivers are
included with support for the following Kernel RDMA drivers:
 - bnxt_re.ko
 - efa.ko
 - erdma.ko
 - iw_cxgb3.ko
 - iw_cxgb4.ko
 - hfi1.ko
 - hns-roce.ko
 - ib_qib.ko
 - irdma.ko
 - mana_ib.ko
 - mlx4_ib.ko
 - mlx5_ib.ko
 - ib_mthca.ko
 - iw_nes.ko
 - ocrdma.ko
 - qedr.ko
 - rdma_rxe.ko
 - siw.ko
 - vmw_pvrdma.ko

Additional service daemons are provided for:
 - srp_daemon (ib_srp.ko)
 - iwpmd (for iwarp kernel providers)
 - ibacm (for InfiniBand communication management assistant)

%description -l pl.UTF-8
Ten pakiet zawiera komponenty przestrzeni użykownika dla podsystemu
drivers/infiniband jądra Linuksa. W szczególności zawiera biblioteki
przestrzeni użytkownika dla następujących urządzeń:
 - /dev/infiniband/uverbsX (libibverbs)
 - /dev/infiniband/rdma_cm (librdmacm)
 - /dev/infiniband/umadX (libibumad)

Dołączony jest komponent przestrzeni użytkownika dla sterowników RDMA
libibverbs w jądrze dla następujących sterowników RDMA z jądra:
 - bnxt_re.ko
 - efa.ko
 - erdma.ko
 - iw_cxgb3.ko
 - iw_cxgb4.ko
 - hfi1.ko
 - hns-roce.ko
 - ib_qib.ko
 - irdma.ko
 - mana_ib.ko
 - mlx4_ib.ko
 - mlx5_ib.ko
 - ib_mthca.ko
 - iw_nes.ko
 - ocrdma.ko
 - qedr.ko
 - rdma_rxe.ko
 - siw.ko
 - vmw_pvrdma.ko

Są także demony dodatkowych usług:
 - srp_daemon (ib_srp.ko)
 - iwpmd (dla sterowników iwarp)
 - ibacm (dla asystenta zarządzania komunikacją InfiniBand)

%package -n rdma-boot
Summary:	RDMA systemd units and udev rules to initialize kernel modules
Summary(pl.UTF-8):	Jednostki systemd i reguły udev do zainicjowania modułów jądra RDMA
Group:		Base
Requires:	systemd-units

%description -n rdma-boot
RDMA systemd units and udev rules to initialize kernel modules.

%description -n rdma-boot -l pl.UTF-8
Jednostki systemd i reguły udev do zainicjowania modułów jądra RDMA.

%package -n rdma-ndd
Summary:	RDMA-NDD - RDMA device Node Description update daemon
Summary(pl.UTF-8):	RDMA-NDD - demon uaktualniający opisy węzłów urządzeń RDMA
Group:		Daemons
Requires:	systemd-units
Requires:	udev-core

%description -n rdma-ndd
RDMA device Node Description update daemon.

%description -n rdma-ndd -l pl.UTF-8
Demon uaktualniający opisy węzłów urządzeń RDMA.

%package -n libibverbs
Summary:	A library for direct userspace use of InfiniBand hardware
Summary(pl.UTF-8):	Biblioteka bezpośredniego dostępu do sprzętu InfiniBand z przestrzeni użytkownika
Group:		Libraries

%description -n libibverbs
libibverbs is a library that allows userspace processes to use
InfiniBand "verbs" as described in the InfiniBand Architecture
Specification. This includes direct hardware access for fast path
operations.

For this library to be useful, a device-specific plug-in module should
also be installed.

%description -n libibverbs -l pl.UTF-8
libibverbs to biblioteka pozwalająca procesom przestrzeni użytkownika
używać metod "verbs" InfiniBand opisanej w specyfikacji architektury
InfiniBand. Obejmuje to bezpośredni dostęp do sprzętu dla operacji po
szybkiej ścieżce.

Aby ta biblioteka była użyteczna powinien być zainstalowany także
odpowiedni moduł dla używanego sprzętu.

%package -n libibverbs-devel
Summary:	Development files for libibverbs library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libibverbs
Group:		Development/Libraries
Requires:	libibverbs = %{version}-%{release}
Requires:	libnl-devel >= 1:3.2

%description -n libibverbs-devel
Header files for libibverbs library.

%description -n libibverbs-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libibverbs.

%package -n libibverbs-static
Summary:	Static libibverbs library
Summary(pl.UTF-8):	Statyczna biblioteka libibverbs
Group:		Development/Libraries
Requires:	libibverbs-devel = %{version}-%{release}
Obsoletes:	libibverbs-devel-static < 1.1.2

%description -n libibverbs-static
Static libibverbs library.

%description -n libibverbs-static -l pl.UTF-8
Statyczna biblioteka libibverbs.

%package -n libibverbs-utils
Summary:	Examples for the libibverbs library
Summary(pl.UTF-8):	Przykładowe programy do biblioteki libibverbs
Group:		Applications/System
Requires:	libibverbs = %{version}-%{release}

%description -n libibverbs-utils
Useful libibverbs example programs such as ibv_devinfo, which
displays information about InfiniBand devices.

%description -n libibverbs-utils -l pl.UTF-8
Przydatne programy przykładowe do biblioteki libibverbs, takie jak
ibv_devinfo wyświetlający informacje o urządzeniach InfiniBand.

%package -n libibverbs-driver-bnxt_re
Summary:	Userspace driver for Broadcom NetXtreme-E HCAs
Summary(pl.UTF-8):	Sterownik przestrzeni użytkownika dla kart HCA Broadcom NetXtreme-E
Group:		Libraries
Requires:	libibverbs = %{version}-%{release}

%description -n libibverbs-driver-bnxt_re
Userspace driver for Broadcom NetXtreme-E HCAs.

%description -n libibverbs-driver-bnxt_re -l pl.UTF-8
Sterownik przestrzeni użytkownika dla kart HCA Broadcom NetXtreme-E.

%package -n libibverbs-driver-bnxt_re-static
Summary:	Static version of bnxt_re driver
Summary(pl.UTF-8):	Statyczna wersja sterownika bnxt_re
Group:		Development/Libraries
Requires:	libibverbs-static = %{version}-%{release}

%description -n libibverbs-driver-bnxt_re-static
Static version of bnxt_re driver, which may be linked directly into
application.

%description -n libibverbs-driver-bnxt_re-static -l pl.UTF-8
Statyczna wersja sterownika bnxt_re, którą można wbudować bezpośrednio
w aplikację.

%package -n libibverbs-driver-cxgb3
Summary:	Userspace driver for the Chelsio T3 iWARP RNIC
Summary(pl.UTF-8):	Sterownik przestrzeni użytkownika dla kart Chelsio T3 iWARP RNIC
Group:		Libraries
Requires:	libibverbs = %{version}-%{release}

%description -n libibverbs-driver-cxgb3
Userspace driver for the Chelsio T3 iWARP RNIC.

%description -n libibverbs-driver-cxgb3 -l pl.UTF-8
Sterownik przestrzeni użytkownika dla kart Chelsio T3 iWARP RNIC.

%package -n libibverbs-driver-cxgb3-static
Summary:	Static version of cxgb3 driver
Summary(pl.UTF-8):	Statyczna wersja sterownika cxgb3
Group:		Development/Libraries
Requires:	libibverbs-static = %{version}-%{release}

%description -n libibverbs-driver-cxgb3-static
Static version of cxgb3 driver, which may be linked directly into
application.

%description -n libibverbs-driver-cxgb3-static -l pl.UTF-8
Statyczna wersja sterownika cxgb3, którą można wbudować bezpośrednio w
aplikację.

%package -n libibverbs-driver-cxgb4
Summary:	Userspace driver for the Chelsio T4 iWARP RNIC
Summary(pl.UTF-8):	Sterownik przestrzeni użytkownika dla kart Chelsio T4 iWARP RNIC
Group:		Libraries
Requires:	libibverbs = %{version}-%{release}

%description -n libibverbs-driver-cxgb4
libcxgb4 is a userspace driver for the Chelsio T4 iWARP RNIC. It works
as a plug-in module for libibverbs that allows programs to use Chelsio
RNICs directly from userspace.

%description -n libibverbs-driver-cxgb4 -l pl.UTF-8
libcxgb4 to sterownik przestrzeni użytkownika dla kart Chelsio T4
iWARP RNIC. Działa jako moduł ładowany przez libibverbs, pozwalający
programom na dostęp z przestrzeni użytkownika do interfejsów RNIC
Chelsio.

%package -n libibverbs-driver-cxgb4-static
Summary:	Static version of cxgb4 driver
Summary(pl.UTF-8):	Statyczna wersja sterownika cxgb4
Group:		Development/Libraries
Requires:	libibverbs-static = %{version}-%{release}

%description -n libibverbs-driver-cxgb4-static
Static version of cxgb4 driver, which may be linked directly into
application.

%description -n libibverbs-driver-cxgb4-static -l pl.UTF-8
Statyczna wersja sterownika cxgb4, którą można wbudować bezpośrednio w
aplikację.

%package -n libibverbs-driver-efa
Summary:	Userspace driver for the Amazon Elastic Fabric Adapters
Summary(pl.UTF-8):	Sterownik przestrzeni użytkownika dla urządzeń Amazon Elastic Fabric Adapter
Group:		Libraries
Requires:	libibverbs-driver-efa-libs = %{version}-%{release}

%description -n libibverbs-driver-efa
libefa is a userspace driver for Amazon Elastic Fabric Adapters. It
works as a plug-in module for libibverbs that allows programs to
use Amazon hardware directly from userspace.

%description -n libibverbs-driver-efa -l pl.UTF-8
libefa to sterownik przestrzeni użytkownika dla urządzeń Amazon
Elastic Fabric Adapter. Działa jako moduł ładowany przez libibverbs,
pozwalający programom na dostęp z przestrzeni użytkownika do sprzętu
Amazona.

%package -n libibverbs-driver-efa-libs
Summary:	Shared library for the Amazon Elastic Fabric Adapters
Summary(pl.UTF-8):	Biblioteka współdzielona dla urządzeń Amazon Elastic Fabric Adapter
Group:		Libraries
Requires:	libibverbs = %{version}-%{release}

%description -n libibverbs-driver-efa-libs
Shared library for the Amazon Elastic Fabric Adapters.

%description -n libibverbs-driver-efa-libs -l pl.UTF-8
Biblioteka współdzielona dla urządzeń Amazon Elastic Fabric Adapter.

%package -n libibverbs-driver-efa-devel
Summary:	Header file for the Amazon Elastic Fabric Adapters library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki dla urządzeń Amazon Elastic Fabric Adapter
Group:		Development/Libraries
Requires:	libibverbs-devel = %{version}-%{release}
Requires:	libibverbs-driver-efa-libs = %{version}-%{release}

%description -n libibverbs-driver-efa-devel
Header file for the Amazon Elastic Fabric Adapters library.

%description -n libibverbs-driver-efa-devel -l pl.UTF-8
Plik nagłówkowy biblioteki dla urządzeń Amazon Elastic Fabric Adapter.

%package -n libibverbs-driver-efa-static
Summary:	Static version of efa driver
Summary(pl.UTF-8):	Statyczna wersja sterownika efa
Group:		Development/Libraries
Requires:	libibverbs-static = %{version}-%{release}

%description -n libibverbs-driver-efa-static
Static version of efa driver, which may be linked directly into
application.

%description -n libibverbs-driver-efa-static -l pl.UTF-8
Statyczna wersja sterownika efa, którą można wbudować bezpośrednio
w aplikację.

%package -n libibverbs-driver-erdma
Summary:	Userspace driver for Alibaba Elastic RDMA (iWarp)  adapters
Summary(pl.UTF-8):	Sterownik przestrzeni użytkownika dla kart Alibaba Elastic RDMA (iWarp) 
Group:		Libraries
Requires:	libibverbs = %{version}-%{release}

%description -n libibverbs-driver-erdma
Userspace driver for Alibaba Elastic RDMA (iWarp)  adapters.

%description -n libibverbs-driver-erdma -l pl.UTF-8
Sterownik przestrzeni użytkownika dla kart Alibaba Elastic RDMA
(iWarp).

%package -n libibverbs-driver-erdma-static
Summary:	Static version of erdma driver
Summary(pl.UTF-8):	Statyczna wersja sterownika erdma
Group:		Development/Libraries
Requires:	libibverbs-static = %{version}-%{release}

%description -n libibverbs-driver-erdma-static
Static version of erdma driver, which may be linked directly into
application.

%description -n libibverbs-driver-erdma-static -l pl.UTF-8
Statyczna wersja sterownika erdma, którą można wbudować bezpośrednio w
aplikację.

%package -n libibverbs-driver-hfi1verbs
Summary:	Userspace driver for Intel OPA Gen1 adapters
Summary(pl.UTF-8):	Sterownik przestrzeni użytkownika dla kart Intel OPA Gen1
Group:		Libraries
Requires:	libibverbs = %{version}-%{release}

%description -n libibverbs-driver-hfi1verbs
Userspace driver for Intel OPA Gen1 adapters.

%description -n libibverbs-driver-hfi1verbs -l pl.UTF-8
Sterownik przestrzeni użytkownika dla kart Intel OPA Gen1.

%package -n libibverbs-driver-hfi1verbs-static
Summary:	Static version of hfi1verbs driver
Summary(pl.UTF-8):	Statyczna wersja sterownika hfi1verbs
Group:		Development/Libraries
Requires:	libibverbs-static = %{version}-%{release}

%description -n libibverbs-driver-hfi1verbs-static
Static version of hfi1verbs driver, which may be linked directly into
application.

%description -n libibverbs-driver-hfi1verbs-static -l pl.UTF-8
Statyczna wersja sterownika hfi1verbs, którą można wbudować
bezpośrednio w aplikację.

%package -n libibverbs-driver-hns
Summary:	Userspace driver for Hisilicon RoCE devices
Summary(pl.UTF-8):	Sterownik przestrzeni użytkownika dla urządzeń Hisilicon RoCE
Group:		Libraries
Requires:	libibverbs = %{version}-%{release}

%description -n libibverbs-driver-hns
Userspace driver for Hisilicon RoCE devices.

%description -n libibverbs-driver-hns -l pl.UTF-8
Sterownik przestrzeni użytkownika dla urządzeń Hisilicon RoCE.

%package -n libibverbs-driver-hns-static
Summary:	Static version of hns driver
Summary(pl.UTF-8):	Statyczna wersja sterownika hns
Group:		Development/Libraries
Requires:	libibverbs-static = %{version}-%{release}

%description -n libibverbs-driver-hns-static
Static version of hns driver, which may be linked directly into
application.

%description -n libibverbs-driver-hns-static -l pl.UTF-8
Statyczna wersja sterownika hns, którą można wbudować bezpośrednio w
aplikację.

%package -n libibverbs-driver-ipathverbs
Summary:	Userspace driver for the QLogic InfiniBand HCAs
Summary(pl.UTF-8):	Sterownik przestrzeni użytkownika dla kart QLogic InfiniBand HCA
Group:		Libraries
Requires:	libibverbs = %{version}-%{release}

%description -n libibverbs-driver-ipathverbs
libipathverbs is a userspace driver for QLogic InfiniBand HCAs. It
works as a plug-in module for libibverbs that allows programs to use
QLogic hardware directly from userspace.

Currently the driver supports the following HCAs:
- InfiniPath QLE7140 (PCIe)
- InfiniPath QMI7140 (PCIe)
- InfiniPath QHT7040 (HyperTransport)
- InfiniPath QHT7140 (HyperTransport)

It uses ib_ipath kernel driver.

%description -n libibverbs-driver-ipathverbs -l pl.UTF-8
libipathverbs to sterownik przestrzeni użytkownika dla kart QLogic
InfiniBand HCA. Działa jako moduł ładowany przez libibverbs,
pozwalający programom na dostęp z przestrzeni użytkownika do sprzętu
QLogic.

Obecnie sterownik obsługuje następujące kontrolery HCA:
- InfiniPath QLE7140 (PCIe)
- InfiniPath QMI7140 (PCIe)
- InfiniPath QHT7040 (HyperTransport)
- InfiniPath QHT7140 (HyperTransport)

Wykorzystuje sterownik jądra ib_ipath.

%package -n libibverbs-driver-ipathverbs-static
Summary:	Static version of ipathverbs driver
Summary(pl.UTF-8):	Statyczna wersja sterownika ipathverbs
Group:		Development/Libraries
Requires:	libibverbs-static = %{version}-%{release}

%description -n libibverbs-driver-ipathverbs-static
Static version of ipathverbs driver, which may be linked directly into
application.

%description -n libibverbs-driver-ipathverbs-static -l pl.UTF-8
Statyczna wersja sterownika ipathverbs, którą można wbudować
bezpośrednio w aplikację.

%package -n libibverbs-driver-irdma
Summary:	Userspace driver for the Intel Ethernet Connection E810 and X722 RDMA adapters
Summary(pl.UTF-8):	Sterownik przestrzeni użytkownika dla kart RDMA Intel Ethernet Connection E810 i X722
Group:		Libraries
Requires:	libibverbs = %{version}-%{release}
Obsoletes:	libibverbs-driver-i40iw < 37.1

%description -n libibverbs-driver-irdma
libirdma is a userspace driver for the Intel Ethernet Connection E810
and X722 RDMA adapters. It works as a plug-in module for libibverbs
that allows programs to use RDMA hardware directly from userspace.

%description -n libibverbs-driver-irdma -l pl.UTF-8
libirdma to sterownik przestrzeni użytkownika dla kart RDMA Intel
Ethernet Connection E810 i X722. Działa jako moduł ładowany przez
libibverbs, pozwalający programom na dostęp z przestrzeni użytkownika
do sprzętu RDMA.

%package -n libibverbs-driver-irdma-static
Summary:	Static version of irdma driver
Summary(pl.UTF-8):	Statyczna wersja sterownika irdma
Group:		Development/Libraries
Requires:	libibverbs-static = %{version}-%{release}
Obsoletes:	libibverbs-driver-i40iw-static < 37.1

%description -n libibverbs-driver-irdma-static
Static version of irdma driver, which may be linked directly into
application.

%description -n libibverbs-driver-irdma-static -l pl.UTF-8
Statyczna wersja sterownika irdma, którą można wbudować bezpośrednio
w aplikację.

%package -n libibverbs-driver-mana
Summary:	Userspace driver for Microsoft Azure Network Adapter
Summary(pl.UTF-8):	Sterownik przestrzeni użytkownika dla kart Microsoft Azure Network Adapter
Group:		Libraries
Requires:	libibverbs-driver-mana-libs = %{version}-%{release}

%description -n libibverbs-driver-mana
libmana is a userspace driver for Microsoft Azure Network Adapters.
It works as a plug-in module for libibverbs that allows programs to
use Mellanox hardware directly from userspace.

%description -n libibverbs-driver-mana -l pl.UTF-8
libmana to sterownik przestrzeni użytkownika dla kart Microsoft Azure
Network Adapter. Działa jako moduł ładowany przez libibverbs,
pozwalający programom na dostęp z przestrzeni użytkownika do sprzętu
Mellanox.

%package -n libibverbs-driver-mana-libs
Summary:	Shared library for Microsoft Azure Network Adapter
Summary(pl.UTF-8):	Biblioteka współdzielona dla kart Microsoft Azure Network Adapter
Group:		Libraries
Requires:	libibverbs = %{version}-%{release}

%description -n libibverbs-driver-mana-libs
Shared library for Microsoft Azure Network Adapter.

%description -n libibverbs-driver-mana-libs -l pl.UTF-8
Biblioteka współdzielona dla kart Microsoft Azure Network Adapter.

%package -n libibverbs-driver-mana-devel
Summary:	Header file for Microsoft Azure Network Adapter library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki dla kart Microsoft Azure Network Adapter
Group:		Development/Libraries
Requires:	libibverbs-devel = %{version}-%{release}
Requires:	libibverbs-driver-mana-libs = %{version}-%{release}

%description -n libibverbs-driver-mana-devel
Header file for the Microsoft Azure Network Adapter library.

%description -n libibverbs-driver-mana-devel -l pl.UTF-8
Plik nagłówkowy biblioteki dla kart Microsoft Azure Network Adapter.

%package -n libibverbs-driver-mana-static
Summary:	Static version of mana driver
Summary(pl.UTF-8):	Statyczna wersja sterownika mana
Group:		Development/Libraries
Requires:	libibverbs-static = %{version}-%{release}

%description -n libibverbs-driver-mana-static
Static version of mana driver, which may be linked directly into
application.

%description -n libibverbs-driver-mana-static -l pl.UTF-8
Statyczna wersja sterownika mana, którą można wbudować bezpośrednio
w aplikację.

%package -n libibverbs-driver-mlx4
Summary:	Userspace driver for the Mellanox ConnectX InfiniBand HCAs
Summary(pl.UTF-8):	Sterownik przestrzeni użytkownika dla kart Mellanox ConnectX InfiniBand HCA
Group:		Libraries
Requires:	libibverbs-driver-mlx4-libs = %{version}-%{release}

%description -n libibverbs-driver-mlx4
libmlx4 is a userspace driver for Mellanox ConnectX InfiniBand HCAs.
It works as a plug-in module for libibverbs that allows programs to
use Mellanox hardware directly from userspace.

Currently the driver supports HCAs on PCI Express interface based on
MT25408 ConnectX chip, using mlx4_ib kernel driver.

%description -n libibverbs-driver-mlx4 -l pl.UTF-8
libmlx4 to sterownik przestrzeni użytkownika dla kart Mellanox
ConnectX InfiniBand HCA. Działa jako moduł ładowany przez libibverbs,
pozwalający programom na dostęp z przestrzeni użytkownika do sprzętu
Mellanox.

Obecnie sterownik obsługuje kontrolery HCA na szynie PCI Express
oparte na układzie MT25408 ConnectX poprzez sterownik jądra mlx4_ib.

%package -n libibverbs-driver-mlx4-libs
Summary:	Shared library for the Mellanox ConnectX InfiniBand HCAs
Summary(pl.UTF-8):	Biblioteka współdzielona dla kart Mellanox ConnectX InfiniBand HCA
Group:		Libraries
Requires:	libibverbs = %{version}-%{release}

%description -n libibverbs-driver-mlx4-libs
Shared library for the Mellanox ConnectX InfiniBand HCAs.

%description -n libibverbs-driver-mlx4-libs -l pl.UTF-8
Biblioteka współdzielona dla kart Mellanox ConnectX InfiniBand HCA.

%package -n libibverbs-driver-mlx4-devel
Summary:	Header file for the Mellanox ConnectX InfiniBand HCAs library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki dla kart Mellanox ConnectX InfiniBand HCA
Group:		Development/Libraries
Requires:	libibverbs-devel = %{version}-%{release}
Requires:	libibverbs-driver-mlx4-libs = %{version}-%{release}

%description -n libibverbs-driver-mlx4-devel
Header file for the Mellanox ConnectX InfiniBand HCAs library.

%description -n libibverbs-driver-mlx4-devel -l pl.UTF-8
Plik nagłówkowy biblioteki dla kart Mellanox ConnectX InfiniBand HCA.

%package -n libibverbs-driver-mlx4-static
Summary:	Static version of mlx4 driver
Summary(pl.UTF-8):	Statyczna wersja sterownika mlx4
Group:		Development/Libraries
Requires:	libibverbs-static = %{version}-%{release}

%description -n libibverbs-driver-mlx4-static
Static version of mlx4 driver, which may be linked directly into
application.

%description -n libibverbs-driver-mlx4-static -l pl.UTF-8
Statyczna wersja sterownika mlx4, którą można wbudować bezpośrednio
w aplikację.

%package -n libibverbs-driver-mlx5
Summary:	Userspace driver for the Mellanox Connect-IB InfiniBand HCAs
Summary(pl.UTF-8):	Sterownik przestrzeni użytkownika dla kart Mellanox Connect-IB InfiniBand HCA
Group:		Libraries
Requires:	libibverbs = %{version}-%{release}

%description -n libibverbs-driver-mlx5
libmlx5 is a userspace driver for Mellanox Connect-IB InfiniBand
HCAs.  It works as a plug-in module for libibverbs that allows
programs to use Mellanox hardware directly from userspace.

Currently the driver supports HCAs on PCI Express interface based on
MT27600 Connect-IB chip, using mlx5_ib kernel driver.

%description -n libibverbs-driver-mlx5 -l pl.UTF-8
libmlx5 to sterownik przestrzeni użytkownika dla kart Mellanox
Connect-IB InfiniBand HCA. Działa jako moduł ładowany przez
libibverbs, pozwalający programom na dostęp z przestrzeni użytkownika
do sprzętu Mellanox.

Obecnie sterownik obsługuje kontrolery HCA na szynie PCI Express
oparte na układzie MT27600 Connect-IB poprzez sterownik jądra mlx5_ib.

%package -n libibverbs-driver-mlx5-libs
Summary:	Shared library for the Mellanox Connect-IB InfiniBand HCAs
Summary(pl.UTF-8):	Biblioteka współdzielona dla kart Mellanox Connect-IB InfiniBand HCA
Group:		Libraries
Requires:	libibverbs = %{version}-%{release}

%description -n libibverbs-driver-mlx5-libs
Shared library for the Mellanox Connect-IB InfiniBand HCAs.

%description -n libibverbs-driver-mlx5-libs -l pl.UTF-8
Biblioteka współdzielona dla kart Mellanox Connect-IB InfiniBand HCA.

%package -n libibverbs-driver-mlx5-devel
Summary:	Header file for the Mellanox Connect-IB InfiniBand HCAs library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki dla kart Mellanox Connect-IB InfiniBand HCA
Group:		Development/Libraries
Requires:	libibverbs-devel = %{version}-%{release}
Requires:	libibverbs-driver-mlx5-libs = %{version}-%{release}

%description -n libibverbs-driver-mlx5-devel
Header file for the Mellanox Connect-IB InfiniBand HCAs library.

%description -n libibverbs-driver-mlx5-devel -l pl.UTF-8
Plik nagłówkowy biblioteki dla kart Mellanox Connect-IB InfiniBand
HCA.

%package -n libibverbs-driver-mlx5-static
Summary:	Static version of mlx5 driver
Summary(pl.UTF-8):	Statyczna wersja sterownika mlx5
Group:		Development/Libraries
Requires:	libibverbs-static = %{version}-%{release}

%description -n libibverbs-driver-mlx5-static
Static version of mlx5 driver, which may be linked directly into
application.

%description -n libibverbs-driver-mlx5-static -l pl.UTF-8
Statyczna wersja sterownika mlx5, którą można wbudować bezpośrednio
w aplikację.

%package -n libibverbs-driver-mthca
Summary:	Userspace driver for the Mellanox InfiniBand HCAs
Summary(pl.UTF-8):	Sterownik przestrzeni użytkownika dla kart Mellanox InfiniBand HCA
Group:		Libraries
Requires:	libibverbs = %{version}-%{release}

%description -n libibverbs-driver-mthca
libmthca is a userspace driver for Mellanox InfiniBand HCAs. It works
as a plug-in module for libibverbs that allows programs to use
Mellanox hardware directly from userspace.

Currently the driver supports HCAs on PCI-X/PCI Express interface
based on MT23108/MT25208/MT25204 InfiniHost chips, using ib_mthca
kernel driver.

%description -n libibverbs-driver-mthca -l pl.UTF-8
libmthca to sterownik przestrzeni użytkownika dla kart Mellanox
InfiniBand HCA. Działa jako moduł ładowany przez libibverbs,
pozwalający programom na dostęp z przestrzeni użytkownika do sprzętu
Mellanox.

Obecnie sterownik obsługuje kontrolery HCA na szynie PCI-X/PCI Express
oparte na układach MT23108/MT25208/MT25204 InfiniHost poprzez
sterownik jądra ib_mthca.

%package -n libibverbs-driver-mthca-static
Summary:	Static version of mthca driver
Summary(pl.UTF-8):	Statyczna wersja sterownika mthca
Group:		Development/Libraries
Requires:	libibverbs-static = %{version}-%{release}

%description -n libibverbs-driver-mthca-static
Static version of mthca driver, which may be linked directly into
application.

%description -n libibverbs-driver-mthca-static -l pl.UTF-8
Statyczna wersja sterownika mthca, którą można wbudować bezpośrednio
w aplikację.

%package -n libibverbs-driver-nes
Summary:	Userspace driver for the NetEffect Ethernet Server Cluster adapters
Summary(pl.UTF-8):	Sterownik przestrzeni użytkownika dla kart NetEffect Ethernet Server Cluster
Group:		Libraries
Requires:	libibverbs = %{version}-%{release}

%description -n libibverbs-driver-nes
libnes is a userspace driver for NetEffect Ethernet Server Cluster
adapters. It works as a plug-in module for libibverbs that allows
programs to use NetEffect hardware directly from userspace.

%description -n libibverbs-driver-nes -l pl.UTF-8
libnes to sterownik przestrzeni użytkownika dla kart NetEffect
Ethernet Server Cluster. Działa jako moduł ładowany przez libibverbs,
pozwalający programom na dostęp z przestrzeni użytkownika do sprzętu
NetEffect.

%package -n libibverbs-driver-nes-static
Summary:	Static version of nes driver
Summary(pl.UTF-8):	Statyczna wersja sterownika nes
Group:		Development/Libraries
Requires:	libibverbs-static = %{version}-%{release}

%description -n libibverbs-driver-nes-static
Static version of nes driver, which may be linked directly into
application.

%description -n libibverbs-driver-nes-static -l pl.UTF-8
Statyczna wersja sterownika nes, którą można wbudować bezpośrednio
w aplikację.

%package -n libibverbs-driver-ocrdma
Summary:	Userspace driver for the Emulex OneConnect RDMA adapters
Summary(pl.UTF-8):	Sterownik przestrzeni użytkownika dla kart Emulex OneConnect RDMA
Group:		Libraries
Requires:	libibverbs = %{version}-%{release}

%description -n libibverbs-driver-ocrdma
libocrdma is a userspace driver for the Emulex OneConnect RDMA
adapters. It works as a plug-in module for libibverbs that allows
programs to use Emulex RDMA hardware directly from userspace.

%description -n libibverbs-driver-ocrdma -l pl.UTF-8
libocrdma to sterownik przestrzeni użytkownika dla kart Emulex
OneConnect RDMA. Działa jako moduł ładowany przez libibverbs,
pozwalający programom na dostęp z przestrzeni użytkownika do
sprzętu Emulex RDMA.

%package -n libibverbs-driver-ocrdma-static
Summary:	Static version of ocrdma driver
Summary(pl.UTF-8):	Statyczna wersja sterownika ocrdma
Group:		Development/Libraries
Requires:	libibverbs-static = %{version}-%{release}

%description -n libibverbs-driver-ocrdma-static
Static version of ocrdma driver, which may be linked directly into
application.

%description -n libibverbs-driver-ocrdma-static -l pl.UTF-8
Statyczna wersja sterownika ocrdma, którą można wbudować bezpośrednio
w aplikację.

%package -n libibverbs-driver-qedr
Summary:	Userspace driver for QLogic QED HCAs
Summary(pl.UTF-8):	Sterownik przestrzeni użytkownika dla kart HCA QLogic QED
Group:		Libraries
Requires:	libibverbs = %{version}-%{release}

%description -n libibverbs-driver-qedr
Userspace driver for QLogic QED HCAs.

%description -n libibverbs-driver-qedr -l pl.UTF-8
Sterownik przestrzeni użytkownika dla kart HCA QLogic QED.

%package -n libibverbs-driver-qedr-static
Summary:	Static version of qedr driver
Summary(pl.UTF-8):	Statyczna wersja sterownika qedr
Group:		Development/Libraries
Requires:	libibverbs-static = %{version}-%{release}

%description -n libibverbs-driver-qedr-static
Static version of qedr driver, which may be linked directly into
application.

%description -n libibverbs-driver-qedr-static -l pl.UTF-8
Statyczna wersja sterownika qedr, którą można wbudować bezpośrednio w
aplikację.

%package -n libibverbs-driver-rxe
Summary:	Userspace driver for software RDMA over Ethernet
Summary(pl.UTF-8):	Sterownik przestrzeni użytkownika dla programowego RDMA po Ethernecie
Group:		Libraries
Requires:	libibverbs = %{version}-%{release}

%description -n libibverbs-driver-rxe
Userspace driver for software RDMA over Ethernet.

%description -n libibverbs-driver-rxe -l pl.UTF-8
Sterownik przestrzeni użytkownika dla programowego RDMA po Ethernecie.

%package -n libibverbs-driver-rxe-static
Summary:	Static version of rxe driver
Summary(pl.UTF-8):	Statyczna wersja sterownika rxe
Group:		Development/Libraries
Requires:	libibverbs-static = %{version}-%{release}

%description -n libibverbs-driver-rxe-static
Static version of rxe driver, which may be linked directly into
application.

%description -n libibverbs-driver-rxe-static -l pl.UTF-8
Statyczna wersja sterownika rxe, którą można wbudować bezpośrednio w
aplikację.

%package -n libibverbs-driver-siw
Summary:	Userspace driver for software iWarp protocol
Summary(pl.UTF-8):	Sterownik przestrzeni użytkownika dla programowego protokołu iWarp
Group:		Libraries
Requires:	libibverbs = %{version}-%{release}

%description -n libibverbs-driver-siw
Userspace driver for software iWarp protocol.

%description -n libibverbs-driver-siw -l pl.UTF-8
Sterownik przestrzeni użytkownika dla programowego protokołu iWarp.

%package -n libibverbs-driver-siw-static
Summary:	Static version of siw driver
Summary(pl.UTF-8):	Statyczna wersja sterownika siw
Group:		Development/Libraries
Requires:	libibverbs-static = %{version}-%{release}

%description -n libibverbs-driver-siw-static
Static version of siw driver, which may be linked directly into
application.

%description -n libibverbs-driver-siw-static -l pl.UTF-8
Statyczna wersja sterownika siw, którą można wbudować bezpośrednio w
aplikację.

%package -n libibverbs-driver-vmw_pvrdma
Summary:	Userspace driver for the VMware Paravirtual RDMA devices
Summary(pl.UTF-8):	Sterownik przestrzeni użytkownika dla urządzeń VMware Paravirtual RDMA
Group:		Libraries
Requires:	libibverbs = %{version}-%{release}

%description -n libibverbs-driver-vmw_pvrdma
libvmw_pvrdma is a userspace driver for VMware Paravirtual RDMA. It
works as a plug-in module for libibverbs that allows programs to use
the VMware Paravirtual RDMA device directly from user space.

%description -n libibverbs-driver-vmw_pvrdma -l pl.UTF-8
libvmw_pvrdma to sterownik przestrzeni użytkownika dla VMware
Paravirtual RDMA. Działa jako moduł ładowany przez libibverbs,
pozwalający programom na dostęp z przestrzeni użytkownika do
urządzeń VMware Paravirtual RDMA.

%package -n libibverbs-driver-vmw_pvrdma-static
Summary:	Static version of vmw_pvrdma driver
Summary(pl.UTF-8):	Statyczna wersja sterownika vmw_pvrdma
Group:		Development/Libraries
Requires:	libibverbs-static = %{version}-%{release}

%description -n libibverbs-driver-vmw_pvrdma-static
Static version of vmw_pvrdma driver, which may be linked directly into
application.

%description -n libibverbs-driver-vmw_pvrdma-static -l pl.UTF-8
Statyczna wersja sterownika vmw_pvrdma, którą można wbudować
bezpośrednio w aplikację.

%package -n librdmacm
Summary:	Userspace RDMA Connection Manager
Summary(pl.UTF-8):	Zarządca połączeń RDMA w przestrzeni użytkowika
Group:		Libraries
Requires:	libibverbs = %{version}-%{release}

%description -n librdmacm
librdmacm provides a userspace RDMA Communication Management API.

%description -n librdmacm -l pl.UTF-8
librdmacm udostępnia API RDMA Communication Management (zarządzające
połączeniami RDMA) w przestrzeni użytkownika.

%package -n librdmacm-devel
Summary:	Header files for librdmacm library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki librdmacm
Group:		Development/Libraries
Requires:	libibverbs-devel = %{version}-%{release}
Requires:	librdmacm = %{version}-%{release}
Requires:	linux-libc-headers >= 7:2.6.20

%description -n librdmacm-devel
Header files for librdmacm library.

%description -n librdmacm-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki librdmacm.

%package -n librdmacm-static
Summary:	Static librdmacm library
Summary(pl.UTF-8):	Statyczna biblioteka librdmacm
Group:		Development/Libraries
Requires:	librdmacm-devel = %{version}-%{release}

%description -n librdmacm-static
This package contains the static librdmacm library.

%description -n librdmacm-static -l pl.UTF-8
Ten pakiet zawiera statyczną bibliotekę librdmacm.

%package -n librdmacm-utils
Summary:	RDMA Connection Manager utilities
Summary(pl.UTF-8):	Programy narzędziowe dla zarządcy połączeń RDMA
Group:		Applications/System
Requires:	librdmacm = %{version}-%{release}

%description -n librdmacm-utils
RDMA Connection Manager utilities.

%description -n librdmacm-utils -l pl.UTF-8
Programy narzędziowe dla zarządcy połączeń RDMA.

%package -n libibumad
Summary:	Userspace InfiniBand MAD library
Summary(pl.UTF-8):	Biblioteka InfiniBand MAD dla przestrzeni użytkownika
Group:		Libraries

%description -n libibumad
libibumad provides the user MAD library functions which sit on top of
the user MAD modules in the kernel. These are used by the IB
diagnostic and management tools, including OpenSM.

%description -n libibumad -l pl.UTF-8
libibumad to biblioteka udostępniająca funkcje MAD w przestrzeni
użytkownika, komunikująca się z modułami MAD w jądrze. Jest używana
przez narzędzia diagnostyczne oraz zarządzające IB, w tym OpenSM.

%package -n libibumad-devel
Summary:	Header files for libibumad library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libibumad
Group:		Development/Libraries
Requires:	libibumad = %{version}-%{release}
# for dir and other IB functionality
Requires:	libibverbs-devel = %{version}-%{release}

%description -n libibumad-devel
Header files for libibumad library.

%description -n libibumad-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libibumad.

%package -n libibumad-static
Summary:	Static libibumad library
Summary(pl.UTF-8):	Statyczna biblioteka libibumad
Group:		Development/Libraries
Requires:	libibumad-devel = %{version}-%{release}

%description -n libibumad-static
This package contains the static libibumad library.

%description -n libibumad-static -l pl.UTF-8
Ten pakiet zawiera statyczną bibliotekę libibumad.

%package -n libibmad
Summary:	OpenFabrics Alliance InfiniBand MAD library
Summary(pl.UTF-8):	Biblioteka OpenFabrics Alliance InfiniBand MAD
Group:		Libraries
Requires:	libibumad = %{version}-%{release}

%description -n libibmad
libibmad provides low layer InfiniBand functions for use by the IB
diagnostic and management programs. These include MAD, SA, SMP, and
other basic IB functions.

%description -n libibmad -l pl.UTF-8
libibmad to biblioteka udostępniająca niskopoziomowe funkcje
InfiniBand przeznaczone dla programów diagnostycznych i zarządzających
IB. Obejmuje MAD, SA, SMP i inne podstawowe funkcje IB.

%package -n libibmad-devel
Summary:	Header files for libibmad library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libibmad
Group:		Development/Libraries
Requires:	libibmad = %{version}-%{release}
Requires:	libibumad-devel = %{version}-%{release}

%description -n libibmad-devel
Header files for libibmad library.

%description -n libibmad-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libibmad.

%package -n libibmad-static
Summary:	Static libibmad library
Summary(pl.UTF-8):	Statyczna biblioteka libibmad
Group:		Development/Libraries
Requires:	libibmad-devel = %{version}-%{release}

%description -n libibmad-static
This package contains the static libibmad library.

%description -n libibmad-static -l pl.UTF-8
Ten pakiet zawiera statyczną bibliotekę libibmad.

%package -n ibacm
Summary:	InfiniBand Communication Manager Assistant
Summary(pl.UTF-8):	Asystent zarządzania komunikacją InfiniBand
Group:		Networking/Utilities
Requires:	rdma-boot = %{version}-%{release}

%description -n ibacm
ibacm assists with establishing communication over InfiniBand.

%description -n ibacm -l pl.UTF-8
ibacm pomaga przy nawiązywaniu łączności poprzez InfiniBand.

%package -n ibacm-devel
Summary:	Header files for IB ACM service
Summary(pl.UTF-8):	Pliki nagłówkowe usługi IB ACM
Group:		Development/Libraries
Requires:	libibverbs-devel = %{version}-%{release}
# doesn't require ibacm

%description -n ibacm-devel
Header files for IB ACM service.

%description -n ibacm-devel -l pl.UTF-8
Pliki nagłówkowe usługi IB ACM.

%package -n infiniband-diags
Summary:	InfiniBand diagnostic tools
Summary(pl.UTF-8):	Narzędzia diagnostyczne InfiniBand
Group:		Networking/Utilities
Requires:	infiniband-diags-libs = %{version}-%{release}

%description -n infiniband-diags
This package provides InfiniBand diagnostic programs and scripts
needed to diagnose an IB subnet.

%description -n infiniband-diags -l pl.UTF-8
Ten pakiet zawiera programy i skrypty diagnostyczne InfiniBand
potrzebne do diagnostyki podsieci IB.

%package -n infiniband-diags-libs
Summary:	InfiniBand diagnostic library
Summary(pl.UTF-8):	Biblioteka diagnostyczna InfiniBand
Group:		Libraries
Requires:	libibmad = %{version}-%{release}
Requires:	libibumad = %{version}-%{release}

%description -n infiniband-diags-libs
InfiniBand diagnostic library.

%description -n infiniband-diags-libs -l pl.UTF-8
Biblioteka diagnostyczna InfiniBand.

%package -n infiniband-diags-devel
Summary:	Header files for libibnetdisc library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libibnetdisc
Group:		Development/Libraries
Requires:	infiniband-diags-libs = %{version}-%{release}
Requires:	libibmad-devel = %{version}-%{release}
Requires:	libibumad-devel = %{version}-%{release}

%description -n infiniband-diags-devel
Header files for libibnetdisc library.

%description -n infiniband-diags-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libibnetdisc.

%package -n infiniband-diags-static
Summary:	Static libibnetdisc library
Summary(pl.UTF-8):	Statyczna biblioteka libibnetdisc
Group:		Development/Libraries
Requires:	infiniband-diags-devel = %{version}-%{release}

%description -n infiniband-diags-static
Static libibnetdisc library.

%description -n infiniband-diags-static -l pl.UTF-8
Statyczna biblioteka libibnetdisc.

%package -n iwpmd
Summary:	iWarp Port Mapper userspace daemon
Summary(pl.UTF-8):	Demon przestrzeni użytkownika usługi iWarp Port Mapper
Group:		Networking/Daemons
Requires:	rc-scripts
Requires:	rdma-boot = %{version}-%{release}
Requires:	systemd-units >= 0.38
# misleading package name before 1.0.6
Obsoletes:	libiwpm < 1.0.6
# internal API headers, never useful without sources
Obsoletes:	libiwpm-devel < 1.0.6

%description -n iwpmd
iwpmd provides a userspace service for iWarp drivers to claim TCP
ports through the standard socket interface.

%description -n iwpmd -l pl.UTF-8
iwpmd dostarcza usługę przestrzeni użytkownika dla sterowników
iWarp, pozwalającą im zajmować porty TCP poprzez standardowy interfejs
gniazdowy.

%package -n srptools
Summary:	Tools for SRP/IB
Summary(pl.UTF-8):	Narzędzia do SRP/IB
Group:		Networking/Utilities
Requires:	rdma-boot = %{version}-%{release}

%description -n srptools
In conjunction with the kernel ib_srp driver, srptools allows you to
discover and use SCSI devices via the SCSI RDMA Protocol over
InfiniBand.

%description -n srptools -l pl.UTF-8
W połączeniu ze sterownikiem jądra ib_srp, srptools pozwalają na
wykrywanie i używanie urządzeń SCSI poprzez protokół SCSI RDMA po
InfiniBand.

%package -n python3-pyverbs
Summary:	Python 3 API over IB verbs
Summary(pl.UTF-8):	API Pythona 3 do IB verbs
Group:		Libraries/Python
Requires:	libibverbs = %{version}-%{release}

%description -n python3-pyverbs
Pyverbs is a Cython-based Python API over libibverbs, providing an
easy, object-oriented access to IB verbs.

%description -n python3-pyverbs -l pl.UTF-8
Pyverbs to oparte na Cythonie API Pythona do libibverbs, zapewniające
łatwy, zorientowany obiektowo dostęp do IB verbs.

%prep
%setup -q
%patch0 -p1
%patch1 -R -p1
%patch2 -R -p1
%patch3 -R -p1
%patch4 -p1

%build
install -d build
cd build
# .pc files generation expect INCLUDEDIR and LIBDIR relative to PREFIX
%cmake .. \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_INITDDIR=/etc/rc.d/init.d \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DCMAKE_INSTALL_PERLDIR=%{perl_vendorlib} \
	-DCMAKE_INSTALL_SYSTEMD_SERVICEDIR=%{systemdunitdir} \
	-DCMAKE_INSTALL_UDEV_RULESDIR=/lib/udev/rules.d \
	%{?with_static_libs:-DENABLE_STATIC=ON} \
%if %{with python}
	-DNO_PYVERBS=OFF \
	-DPYTHON_EXECUTABLE:PATH=%{__python3}
%else
	-DNO_PYVERBS=ON
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
#install -d $RPM_BUILD_ROOT%{_pkgconfigdir}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with python}
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/pyverbs/{tests,run_tests.py}
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}/pyverbs
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}/pyverbs
%endif

# TODO: drop when other packages switch to upstream compatible lib{ibverbs,rdmacm}.pc
# check if not present already
[ ! -f $RPM_BUILD_ROOT%{_pkgconfigdir}/ibverbs.pc ] || exit 1
sed -e 's,@prefix@,%{_prefix},;
	s,@libdir@,%{_libdir},;
	s,@LIBVERSION@,%{version},' %{SOURCE1} >$RPM_BUILD_ROOT%{_pkgconfigdir}/ibverbs.pc
[ ! -f $RPM_BUILD_ROOT%{_pkgconfigdir}/rdmacm.pc ] || exit 1
sed -e 's,@prefix@,%{_prefix},;
	s,@libdir@,%{_libdir},;
	s,@LIBVERSION@,%{version},' %{SOURCE2} >$RPM_BUILD_ROOT%{_pkgconfigdir}/rdmacm.pc

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_docdir}/{MAINTAINERS,*.md,70-persistent-ipoib.rules}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libibverbs -p /sbin/ldconfig
%postun	-n libibverbs -p /sbin/ldconfig

%post	-n libibverbs-driver-efa-libs -p /sbin/ldconfig
%postun	-n libibverbs-driver-efa-libs -p /sbin/ldconfig

%post	-n libibverbs-driver-mana-libs -p /sbin/ldconfig
%postun	-n libibverbs-driver-mana-libs -p /sbin/ldconfig

%post	-n libibverbs-driver-mlx4-libs -p /sbin/ldconfig
%postun	-n libibverbs-driver-mlx4-libs -p /sbin/ldconfig

%post	-n libibverbs-driver-mlx5-libs -p /sbin/ldconfig
%postun	-n libibverbs-driver-mlx5-libs -p /sbin/ldconfig

%post	-n librdmacm -p /sbin/ldconfig
%postun	-n librdmacm -p /sbin/ldconfig

%post	-n libibumad -p /sbin/ldconfig
%postun	-n libibumad -p /sbin/ldconfig

%post	-n libibmad -p /sbin/ldconfig
%postun	-n libibmad -p /sbin/ldconfig

%post	-n infiniband-diags-libs -p /sbin/ldconfig
%postun	-n infiniband-diags-libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
# metapackage

%files -n rdma-boot
%defattr(644,root,root,755)
%doc Documentation/udev.md build/kernel-boot/persistent-ipoib.rules.in
%dir %{_sysconfdir}/rdma
%dir %{_sysconfdir}/rdma/modules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rdma/modules/infiniband.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rdma/modules/iwarp.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rdma/modules/opa.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rdma/modules/rdma.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rdma/modules/roce.conf
%{systemdunitdir}/rdma-hw.target
%{systemdunitdir}/rdma-load-modules@.service
%attr(755,root,root) /lib/udev/rdma_rename
/lib/udev/rules.d/60-rdma-persistent-naming.rules
/lib/udev/rules.d/75-rdma-description.rules
/lib/udev/rules.d/90-rdma-hw-modules.rules
/lib/udev/rules.d/90-rdma-ulp-modules.rules
/lib/udev/rules.d/90-rdma-umad.rules

%files -n rdma-ndd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/rdma-ndd
%{systemdunitdir}/rdma-ndd.service
/lib/udev/rules.d/60-rdma-ndd.rules
%{_mandir}/man8/rdma-ndd.8*

%files -n libibverbs
%defattr(644,root,root,755)
%doc COPYING.BSD_FB COPYING.BSD_MIT COPYING.md MAINTAINERS README.md Documentation/{libibverbs,tag_matching}.md
%attr(755,root,root) %{_libdir}/libibverbs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libibverbs.so.1
%dir %{_libdir}/libibverbs
%dir %{_sysconfdir}/libibverbs.d

%files -n libibverbs-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibverbs.so
%dir %{_includedir}/infiniband
%{_includedir}/infiniband/arch.h
%{_includedir}/infiniband/ib_user_ioctl_verbs.h
%{_includedir}/infiniband/opcode.h
%{_includedir}/infiniband/sa.h
%{_includedir}/infiniband/sa-kern-abi.h
%{_includedir}/infiniband/tm_types.h
%{_includedir}/infiniband/verbs.h
%{_includedir}/infiniband/verbs_api.h
%{_pkgconfigdir}/libibverbs.pc
# backward compat
%{_pkgconfigdir}/ibverbs.pc
%{_mandir}/man3/ibv_*.3*
%{_mandir}/man3/mbps_to_ibv_rate.3*
%{_mandir}/man3/mult_to_ibv_rate.3*

%if %{with static_libs}
%files -n libibverbs-static
%defattr(644,root,root,755)
%{_libdir}/libibverbs.a
%endif

%files -n libibverbs-utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ibv_*
%{_mandir}/man1/ibv_*.1*

%files -n libibverbs-driver-bnxt_re
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibverbs/libbnxt_re-%{ibv_abi}.so
%{_sysconfdir}/libibverbs.d/bnxt_re.driver

%if %{with static_libs}
%files -n libibverbs-driver-bnxt_re-static
%defattr(644,root,root,755)
%{_libdir}/libbnxt_re-%{ibv_abi}.a
%endif

%files -n libibverbs-driver-cxgb3
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibverbs/libcxgb3-%{ibv_abi}.so
%{_sysconfdir}/libibverbs.d/cxgb3.driver

%if %{with static_libs}
%files -n libibverbs-driver-cxgb3-static
%defattr(644,root,root,755)
%{_libdir}/libcxgb3-%{ibv_abi}.a
%endif

%files -n libibverbs-driver-cxgb4
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibverbs/libcxgb4-%{ibv_abi}.so
%{_sysconfdir}/libibverbs.d/cxgb4.driver

%if %{with static_libs}
%files -n libibverbs-driver-cxgb4-static
%defattr(644,root,root,755)
%{_libdir}/libcxgb4-%{ibv_abi}.a
%endif

%files -n libibverbs-driver-efa
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibverbs/libefa-%{ibv_abi}.so
%{_sysconfdir}/libibverbs.d/efa.driver

%files -n libibverbs-driver-efa-libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libefa.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libefa.so.1

%files -n libibverbs-driver-efa-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libefa.so
%{_includedir}/infiniband/efadv.h
%{_pkgconfigdir}/libefa.pc
%{_mandir}/man3/efadv_create_driver_qp.3*
%{_mandir}/man3/efadv_create_qp_ex.3*
%{_mandir}/man3/efadv_query_ah.3*
%{_mandir}/man3/efadv_query_device.3*
%{_mandir}/man7/efadv.7*

%if %{with static_libs}
%files -n libibverbs-driver-efa-static
%defattr(644,root,root,755)
%{_libdir}/libefa.a
%endif

%files -n libibverbs-driver-erdma
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibverbs/liberdma-%{ibv_abi}.so
%{_sysconfdir}/libibverbs.d/erdma.driver

%if %{with static_libs}
%files -n libibverbs-driver-erdma-static
%defattr(644,root,root,755)
%{_libdir}/liberdma-%{ibv_abi}.a
%endif

%files -n libibverbs-driver-hfi1verbs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibverbs/libhfi1verbs-%{ibv_abi}.so
%{_sysconfdir}/libibverbs.d/hfi1verbs.driver

%if %{with static_libs}
%files -n libibverbs-driver-hfi1verbs-static
%defattr(644,root,root,755)
%{_libdir}/libhfi1verbs-%{ibv_abi}.a
%endif

%files -n libibverbs-driver-hns
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibverbs/libhns-%{ibv_abi}.so
%{_sysconfdir}/libibverbs.d/hns.driver

%if %{with static_libs}
%files -n libibverbs-driver-hns-static
%defattr(644,root,root,755)
%{_libdir}/libhns-%{ibv_abi}.a
%endif

%files -n libibverbs-driver-ipathverbs
%defattr(644,root,root,755)
%attr(755,roor,root) %{_libexecdir}/truescale-serdes.cmds
%attr(755,root,root) %{_libdir}/libibverbs/libipathverbs-%{ibv_abi}.so
%{_sysconfdir}/libibverbs.d/ipathverbs.driver
%config(noreplace) %verify(not md5 mtime size) /etc/modprobe.d/truescale.conf

%if %{with static_libs}
%files -n libibverbs-driver-ipathverbs-static
%defattr(644,root,root,755)
%{_libdir}/libipathverbs-%{ibv_abi}.a
%endif

%files -n libibverbs-driver-irdma
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibverbs/libirdma-%{ibv_abi}.so
%{_sysconfdir}/libibverbs.d/irdma.driver

%if %{with static_libs}
%files -n libibverbs-driver-irdma-static
%defattr(644,root,root,755)
%{_libdir}/libirdma-%{ibv_abi}.a
%endif

%files -n libibverbs-driver-mana
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibverbs/libmana-%{ibv_abi}.so
%{_sysconfdir}/libibverbs.d/mana.driver

%files -n libibverbs-driver-mana-libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmana.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmana.so.1

%files -n libibverbs-driver-mana-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmana.so
%{_includedir}/infiniband/manadv.h
%{_pkgconfigdir}/libmana.pc
%{_mandir}/man3/manadv_*.3*
%{_mandir}/man7/manadv.7*

%files -n libibverbs-driver-mana-static
%defattr(644,root,root,755)
%{_libdir}/libmana.a

%files -n libibverbs-driver-mlx4
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibverbs/libmlx4-%{ibv_abi}.so
%{_sysconfdir}/libibverbs.d/mlx4.driver
/etc/modprobe.d/mlx4.conf

%files -n libibverbs-driver-mlx4-libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmlx4.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmlx4.so.1

%files -n libibverbs-driver-mlx4-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmlx4.so
%{_includedir}/infiniband/mlx4dv.h
%{_pkgconfigdir}/libmlx4.pc
%{_mandir}/man3/mlx4dv_*.3*
%{_mandir}/man7/mlx4dv.7*

%if %{with static_libs}
%files -n libibverbs-driver-mlx4-static
%defattr(644,root,root,755)
%{_libdir}/libmlx4.a
%endif

%files -n libibverbs-driver-mlx5
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibverbs/libmlx5-%{ibv_abi}.so
%{_sysconfdir}/libibverbs.d/mlx5.driver

%files -n libibverbs-driver-mlx5-libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmlx5.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmlx5.so.1

%files -n libibverbs-driver-mlx5-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmlx5.so
%{_includedir}/infiniband/mlx5_api.h
%{_includedir}/infiniband/mlx5_user_ioctl_verbs.h
%{_includedir}/infiniband/mlx5dv.h
%{_pkgconfigdir}/libmlx5.pc
%{_mandir}/man3/mlx5dv_*.3*
%{_mandir}/man7/mlx5dv.7*

%if %{with static_libs}
%files -n libibverbs-driver-mlx5-static
%defattr(644,root,root,755)
%{_libdir}/libmlx5.a
%endif

%files -n libibverbs-driver-mthca
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibverbs/libmthca-%{ibv_abi}.so
%{_sysconfdir}/libibverbs.d/mthca.driver

%if %{with static_libs}
%files -n libibverbs-driver-mthca-static
%defattr(644,root,root,755)
%{_libdir}/libmthca-%{ibv_abi}.a
%endif

%files -n libibverbs-driver-nes
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibverbs/libnes-%{ibv_abi}.so
%{_sysconfdir}/libibverbs.d/nes.driver

%if %{with static_libs}
%files -n libibverbs-driver-nes-static
%defattr(644,root,root,755)
%{_libdir}/libnes-%{ibv_abi}.a
%endif

%files -n libibverbs-driver-ocrdma
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibverbs/libocrdma-%{ibv_abi}.so
%{_sysconfdir}/libibverbs.d/ocrdma.driver

%if %{with static_libs}
%files -n libibverbs-driver-ocrdma-static
%defattr(644,root,root,755)
%{_libdir}/libocrdma-%{ibv_abi}.a
%endif

%files -n libibverbs-driver-qedr
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibverbs/libqedr-%{ibv_abi}.so
%{_sysconfdir}/libibverbs.d/qedr.driver

%if %{with static_libs}
%files -n libibverbs-driver-qedr-static
%defattr(644,root,root,755)
%{_libdir}/libqedr-%{ibv_abi}.a
%endif

%files -n libibverbs-driver-rxe
%defattr(644,root,root,755)
%doc Documentation/rxe.md
%attr(755,root,root) %{_libdir}/libibverbs/librxe-%{ibv_abi}.so
%{_sysconfdir}/libibverbs.d/rxe.driver
%{_mandir}/man7/rxe.7*

%if %{with static_libs}
%files -n libibverbs-driver-rxe-static
%defattr(644,root,root,755)
%{_libdir}/librxe-%{ibv_abi}.a
%endif

%files -n libibverbs-driver-siw
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibverbs/libsiw-%{ibv_abi}.so
%{_sysconfdir}/libibverbs.d/siw.driver

%if %{with static_libs}
%files -n libibverbs-driver-siw-static
%defattr(644,root,root,755)
%{_libdir}/libsiw-%{ibv_abi}.a
%endif

%files -n libibverbs-driver-vmw_pvrdma
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibverbs/libvmw_pvrdma-%{ibv_abi}.so
%{_sysconfdir}/libibverbs.d/vmw_pvrdma.driver

%if %{with static_libs}
%files -n libibverbs-driver-vmw_pvrdma-static
%defattr(644,root,root,755)
%{_libdir}/libvmw_pvrdma-%{ibv_abi}.a
%endif

%files -n librdmacm
%defattr(644,root,root,755)
%doc Documentation/librdmacm.md
%attr(755,root,root) %{_libdir}/librdmacm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librdmacm.so.1
%dir %{_libdir}/rsocket
%attr(755,root,root) %{_libdir}/rsocket/librspreload.so*

%files -n librdmacm-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librdmacm.so
%{_includedir}/infiniband/ib.h
%{_includedir}/rdma/rdma_cma.h
%{_includedir}/rdma/rdma_cma_abi.h
%{_includedir}/rdma/rdma_verbs.h
%{_includedir}/rdma/rsocket.h
%{_pkgconfigdir}/librdmacm.pc
# backward compat
%{_pkgconfigdir}/rdmacm.pc
%{_mandir}/man3/rdma_*.3*
%{_mandir}/man7/rdma_cm.7*
%{_mandir}/man7/rsocket.7*

%files -n librdmacm-utils
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cmtime
%attr(755,root,root) %{_bindir}/mckey
%attr(755,root,root) %{_bindir}/rcopy
%attr(755,root,root) %{_bindir}/rdma_client
%attr(755,root,root) %{_bindir}/rdma_server
%attr(755,root,root) %{_bindir}/rdma_xclient
%attr(755,root,root) %{_bindir}/rdma_xserver
%attr(755,root,root) %{_bindir}/riostream
%attr(755,root,root) %{_bindir}/rping
%attr(755,root,root) %{_bindir}/rstream
%attr(755,root,root) %{_bindir}/ucmatose
%attr(755,root,root) %{_bindir}/udaddy
%attr(755,root,root) %{_bindir}/udpong
%{_mandir}/man1/cmtime.1*
%{_mandir}/man1/mckey.1*
%{_mandir}/man1/rcopy.1*
%{_mandir}/man1/rdma_client.1*
%{_mandir}/man1/rdma_server.1*
%{_mandir}/man1/rdma_xclient.1*
%{_mandir}/man1/rdma_xserver.1*
%{_mandir}/man1/riostream.1*
%{_mandir}/man1/rping.1*
%{_mandir}/man1/rstream.1*
%{_mandir}/man1/ucmatose.1*
%{_mandir}/man1/udaddy.1*
%{_mandir}/man1/udpong.1*

%if %{with static_libs}
%files -n librdmacm-static
%defattr(644,root,root,755)
%{_libdir}/librdmacm.a
%endif

%files -n libibumad
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibumad.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libibumad.so.3

%files -n libibumad-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibumad.so
%{_includedir}/infiniband/umad*.h
%{_pkgconfigdir}/libibumad.pc
%{_mandir}/man3/umad_*.3*

%if %{with static_libs}
%files -n libibumad-static
%defattr(644,root,root,755)
%{_libdir}/libibumad.a
%endif

%files -n libibmad
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibmad.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libibmad.so.5

%files -n libibmad-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibmad.so
%{_includedir}/infiniband/mad.h
%{_includedir}/infiniband/mad_osd.h
%{_pkgconfigdir}/libibmad.pc

%if %{with static_libs}
%files -n libibmad-static
%defattr(644,root,root,755)
%{_libdir}/libibmad.a
%endif

%files -n ibacm
%defattr(644,root,root,755)
%doc Documentation/ibacm.md
%attr(755,root,root) %{_bindir}/ib_acme
%attr(755,root,root) %{_sbindir}/ibacm
%dir %{_libdir}/ibacm
%attr(755,root,root) %{_libdir}/ibacm/libibacmp.so
%attr(754,root,root) /etc/rc.d/init.d/ibacm
%{systemdunitdir}/ibacm.service
%{systemdunitdir}/ibacm.socket
%{_mandir}/man1/ib_acme.1*
%{_mandir}/man8/ibacm.8*

%files -n ibacm-devel
%defattr(644,root,root,755)
%{_includedir}/infiniband/acm.h
%{_includedir}/infiniband/acm_prov.h
%{_mandir}/man7/ibacm.7*
%{_mandir}/man7/ibacm_prov.7*

%files -n infiniband-diags
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/check_lft_balance.pl
%attr(755,root,root) %{_sbindir}/dump_fts
%attr(755,root,root) %{_sbindir}/dump_lfts.sh
%attr(755,root,root) %{_sbindir}/dump_mfts.sh
%attr(755,root,root) %{_sbindir}/ibaddr
%attr(755,root,root) %{_sbindir}/ibcacheedit
%attr(755,root,root) %{_sbindir}/ibccconfig
%attr(755,root,root) %{_sbindir}/ibccquery
%attr(755,root,root) %{_sbindir}/ibfindnodesusing.pl
%attr(755,root,root) %{_sbindir}/ibhosts
%attr(755,root,root) %{_sbindir}/ibidsverify.pl
%attr(755,root,root) %{_sbindir}/iblinkinfo
%attr(755,root,root) %{_sbindir}/ibnetdiscover
%attr(755,root,root) %{_sbindir}/ibnodes
%attr(755,root,root) %{_sbindir}/ibping
%attr(755,root,root) %{_sbindir}/ibportstate
%attr(755,root,root) %{_sbindir}/ibqueryerrors
%attr(755,root,root) %{_sbindir}/ibroute
%attr(755,root,root) %{_sbindir}/ibrouters
%attr(755,root,root) %{_sbindir}/ibstat
%attr(755,root,root) %{_sbindir}/ibstatus
%attr(755,root,root) %{_sbindir}/ibswitches
%attr(755,root,root) %{_sbindir}/ibsysstat
%attr(755,root,root) %{_sbindir}/ibtracert
%attr(755,root,root) %{_sbindir}/perfquery
%attr(755,root,root) %{_sbindir}/saquery
%attr(755,root,root) %{_sbindir}/sminfo
%attr(755,root,root) %{_sbindir}/smpdump
%attr(755,root,root) %{_sbindir}/smpquery
%attr(755,root,root) %{_sbindir}/vendstat
%dir %{_sysconfdir}/infiniband-diags
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/infiniband-diags/error_thresholds
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/infiniband-diags/ibdiag.conf
%{perl_vendorlib}/IBswcountlimits.pm
%{_mandir}/man8/check_lft_balance.8*
%{_mandir}/man8/dump_fts.8*
%{_mandir}/man8/dump_lfts.8*
%{_mandir}/man8/dump_mfts.8*
%{_mandir}/man8/ibaddr.8*
%{_mandir}/man8/ibcacheedit.8*
%{_mandir}/man8/ibccconfig.8*
%{_mandir}/man8/ibccquery.8*
%{_mandir}/man8/ibfindnodesusing.8*
%{_mandir}/man8/ibhosts.8*
%{_mandir}/man8/ibidsverify.8*
%{_mandir}/man8/iblinkinfo.8*
%{_mandir}/man8/ibnetdiscover.8*
%{_mandir}/man8/ibnodes.8*
%{_mandir}/man8/ibping.8*
%{_mandir}/man8/ibportstate.8*
%{_mandir}/man8/ibqueryerrors.8*
%{_mandir}/man8/ibroute.8*
%{_mandir}/man8/ibrouters.8*
%{_mandir}/man8/ibstat.8*
%{_mandir}/man8/ibstatus.8*
%{_mandir}/man8/ibswitches.8*
%{_mandir}/man8/ibsysstat.8*
%{_mandir}/man8/ibtracert.8*
%{_mandir}/man8/infiniband-diags.8*
%{_mandir}/man8/perfquery.8*
%{_mandir}/man8/saquery.8*
%{_mandir}/man8/sminfo.8*
%{_mandir}/man8/smpdump.8*
%{_mandir}/man8/smpquery.8*
%{_mandir}/man8/vendstat.8*

%files -n infiniband-diags-libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibnetdisc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libibnetdisc.so.5

%files -n infiniband-diags-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libibnetdisc.so
%{_includedir}/infiniband/ibnetdisc.h
%{_includedir}/infiniband/ibnetdisc_osd.h
%{_pkgconfigdir}/libibnetdisc.pc
%{_mandir}/man3/ibnd_*.3*

%if %{with static_libs}
%files -n infiniband-diags-static
%defattr(644,root,root,755)
%{_libdir}/libibnetdisc.a
%endif

%files -n iwpmd
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/iwpmd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/iwpmd.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rdma/modules/iwpmd.conf
%attr(754,root,root) /etc/rc.d/init.d/iwpmd
%{systemdunitdir}/iwpmd.service
/lib/udev/rules.d/90-iwpmd.rules
%{_mandir}/man5/iwpmd.conf.5*
%{_mandir}/man8/iwpmd.8*

%files -n srptools
%defattr(644,root,root,755)
%doc Documentation/ibsrpdm.md
%attr(755,root,root) %{_sbindir}/srp_daemon
%attr(755,root,root) %{_sbindir}/srp_daemon.sh
%attr(755,root,root) %{_sbindir}/ibsrpdm
%attr(755,root,root) %{_sbindir}/run_srp_daemon
%dir %{_libexecdir}/srp_daemon
%attr(755,roor,root) %{_libexecdir}/srp_daemon/start_on_all_ports
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/srp_daemon.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/rdma/modules/srp_daemon.conf
%attr(754,root,root) /etc/rc.d/init.d/srpd
%{systemdunitdir}/srp_daemon.service
%{systemdunitdir}/srp_daemon_port@.service
/lib/udev/rules.d/60-srp_daemon.rules
%{_mandir}/man5/srp_daemon.service.5*
%{_mandir}/man5/srp_daemon_port@.service.5*
%{_mandir}/man8/ibsrpdm.8*
%{_mandir}/man8/srp_daemon.8*

%if %{with python}
%files -n python3-pyverbs
%defattr(644,root,root,755)
%dir %{py3_sitedir}/pyverbs
%attr(755,root,root) %{py3_sitedir}/pyverbs/*.cpython-*.so
%{py3_sitedir}/pyverbs/*.py
%{py3_sitedir}/pyverbs/__pycache__
%endif
