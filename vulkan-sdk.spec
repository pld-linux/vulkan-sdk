#
# TODO:
#	- investigate why vktrace does not work


# Conditional build:
%bcond_with	tests		# build with tests (require a working Vulkan
				# driver (ICD))
%bcond_without	wayland		# enable Wayland support in loader
%bcond_without	xlib		# enable XLib support in loader

%define	api_version 1.0.39

Summary:	LunarG Vulkan SDK
Name:		vulkan-sdk
Version:	1.0.39.1
Release:	1
License:	MIT-like
Group:		Development
Source0:	https://github.com/LunarG/VulkanTools/archive/sdk-%{version}/VulkanTools-%{version}.tar.gz
# Source0-md5:	62446dfd61208771d39109218cb29152
Patch0:		system_glslang_and_spirv-tools.patch
Patch1:		demos_out_of_src.patch
Patch2:		rpath.patch
Patch3:		always_xcb.patch
Patch4:		x32.patch
Patch5:		system_jsoncpp.patch
URL:		http://lunarg.com/vulkan-sdk/
BuildRequires:	bison
BuildRequires:	cmake
BuildRequires:	GLM
BuildRequires:	glslang >= 3.0.s20161222
BuildRequires:	glslang-devel >= 3.0.s20161222
BuildRequires:	graphviz
BuildRequires:	ImageMagick-devel
BuildRequires:	jsoncpp-devel
BuildRequires:	libpng
BuildRequires:	libxcb-devel
BuildRequires:	python3
BuildRequires:	python3-lxml
BuildRequires:	python3-modules
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5Svg-devel
BuildRequires:	Qt5Widgets-devel
BuildRequires:	spirv-tools-devel >= v2016.7
BuildRequires:	udev-devel
Requires:	glslang >= 3.0.s20161222
Requires:	spirv-tools >= v2016.7
Requires:	%{name}-debug-layers = %{version}-%{release}
Requires:	vulkan-devel = %{version}-%{release}
Requires:	vulkan-loader = %{version}-%{release}
Requires:	vulkan-sdk-tools = %{version}-%{release}
Requires:	%{name}-validation-layers = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Vulkan API Software Development Kit

%package -n vulkan-loader
Summary:	Vulkan API loader
License:	MIT-like
Group:		Library
Provides:	vulkan(loader) = %{api_version}

%description -n vulkan-loader
Common loader for Vulkan API drivers.

%package validation-layers
Summary:	Validation layers for Vulkan
Group:		Development/Libraries
Requires:	vulkan-loader = %{version}-%{release}

%description validation-layers
Validation layers for Vulkan.

%package debug-layers
Summary:	Debug layers for Vulkan
Group:		Development/Libraries
Requires:	vulkan-loader = %{version}-%{release}

%description debug-layers
Debug layers for Vulkan.

%package -n vulkan-devel
Summary:	Header files for the Vulkan API
Summary(pl.UTF-8):	Pliki nagłówkowe API Vulkan
Group:		Development/Libraries
Requires:	vulkan-loader = %{version}-%{release}

%description -n vulkan-devel
Header files for the Vulkan API.

%description -n vulkan-devel -l pl.UTF-8
Pliki nagłówkowe API Vulkan.

%package demos
Summary:	Vulkan demos
Group:		Development/Libraries
Requires:	vulkan(icd)
Requires:	vulkan-loader = %{version}-%{release}

%description demos
Vulkan demos.

%package tools
Summary:	Vulkan tools
Group:		Development
Suggests:	vulkan(icd)
Requires:	vulkan-loader = %{version}-%{release}

%description tools
Vulkan tools.

%package tools-vktraceviewer
Summary:	Vulkan trace viewer
Group:		Development
Requires:	%{name}-tools = %{version}-%{release}

%description tools-vktraceviewer
Vulkan trace viewer.

%prep
%setup -qn VulkanTools-sdk-%{version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
install -d build
cd build

%cmake \
	-DJSONCPP_INCLUDE_DIR=/usr/include/jsoncpp \
	-DJSONCPP_SOURCE_DIR=/usr/include/jsoncpp \
	-DCMAKE_INSTALL_DATADIR=share \
	-DCMAKE_INSTALL_SYSCONFDIR=etc \
	-DBUILD_TESTS=%{?with_tests:ON}%{!?with_tests:OFF} \
	-DBUILD_WSI_WAYLAND_SUPPORT=%{?with_wayland:ON}%{!?with_wayland:OFF} \
	-DBUILD_WSI_XLIB_SUPPORT=%{?with_xlib:ON}%{!?with_xlib:OFF} \
	-DBUILD_WSI_MIR_SUPPORT=OFF \
	-DBUILD_ICD=OFF \
		../
%{__make}

%if %{with tests}
cd tests
LC_ALL=C.utf-8 VK_LAYER_PATH=../layers LD_LIBRARY_PATH=../loader:../layers ./run_all_tests.sh
cd ..
%endif

cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir},%{_sysconfdir}}/vulkan/icd.d \
$RPM_BUILD_ROOT{%{_datadir},%{_sysconfdir}}/vulkan/{explicit,implicit}_layer.d \
	$RPM_BUILD_ROOT%{_bindir} \
	$RPM_BUILD_ROOT%{_includedir}/vulkan \
	$RPM_BUILD_ROOT%{_datadir}/%{name}-demos \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}


# hack for 'make install' tryin to install in relative paths when DESTDIR is set
install -d "$RPM_BUILD_ROOT$PWD"
ln -s "$PWD/build" "$RPM_BUILD_ROOT$PWD"

cd build
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm "$RPM_BUILD_ROOT$PWD"

cp -p demos/vulkaninfo $RPM_BUILD_ROOT%{_bindir}/vulkaninfo
cp -p demos/cube $RPM_BUILD_ROOT%{_bindir}/vulkan-cube
cp -p demos/smoketest $RPM_BUILD_ROOT%{_bindir}/vulkan-smoketest
cp -p demos/{lunarg.ppm,*-vert.spv,*-frag.spv} $RPM_BUILD_ROOT%{_datadir}/%{name}-demos

mv $RPM_BUILD_ROOT/usr/etc/vulkan/explicit_layer.d/* $RPM_BUILD_ROOT%{_datadir}/vulkan/explicit_layer.d

cp -p libs/vkjson/libvkjson.a $RPM_BUILD_ROOT%{_libdir}
cp -p libs/vkjson/vkjson_{info,unittest} $RPM_BUILD_ROOT%{_bindir}

cp -p ../libs/vkjson/vkjson.h $RPM_BUILD_ROOT%{_includedir}

cp -p install_staging/*.so $RPM_BUILD_ROOT%{_libdir}
for f in layersvt/*.json ; do
sed -e's@"library_path": "./@"library_path": "@' $f > $RPM_BUILD_ROOT%{_datadir}/vulkan/explicit_layer.d/$(basename $f)
done

cp -pr ../demos/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# restore original demo sources in %{_examplesdir}
%patch1 -R -p2 -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
rm -f $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/*.orig 2>/dev/null || :

%ifarch %x8664
cp -p vktrace/libVkLayer_vktrace_layer.so $RPM_BUILD_ROOT%{_libdir}
cp -p vktrace/vkreplay $RPM_BUILD_ROOT%{_bindir}
cp -p vktrace/vktrace $RPM_BUILD_ROOT%{_bindir}
sed -e's@"library_path": "../vktrace/@"library_path": "@' \
	layersvt/VkLayer_vktrace_layer.json > $RPM_BUILD_ROOT%{_datadir}/vulkan/explicit_layer.d/VkLayer_vktrace_layer.json
%else
cp -p vktrace/libVkLayer_vktrace_layer32.so $RPM_BUILD_ROOT%{_libdir}
cp -p vktrace/vkreplay32 $RPM_BUILD_ROOT%{_bindir}
cp -p vktrace/vktrace32 $RPM_BUILD_ROOT%{_bindir}
rm $RPM_BUILD_ROOT%{_datadir}/vulkan/explicit_layer.d/VkLayer_vktrace_layer.json
sed -e's@"library_path": "../vktrace/@"library_path": "@' \
    -e's@libVkLayer_vktrace_layer.so@libVkLayer_vktrace_layer32.so@' \
	layersvt/VkLayer_vktrace_layer.json > $RPM_BUILD_ROOT%{_datadir}/vulkan/explicit_layer.d/VkLayer_vktrace_layer32.json
%endif

install via/via $RPM_BUILD_ROOT%{_bindir}
install vktrace/vktraceviewer $RPM_BUILD_ROOT%{_bindir}

cd ..

cp -p vktrace/README.md vktrace-README.md
cp -p vktrace/TODO.md vktrace-TODO.md

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n vulkan-loader -p /sbin/ldconfig
%postun	-n vulkan-loader -p /sbin/ldconfig

%files
%defattr(644,root,root,755)

%files -n vulkan-loader
%defattr(644,root,root,755)
%doc COPYRIGHT.txt LICENSE.txt
%doc loader/{README.md,LoaderAndLayerInterface.md}
%dir %{_sysconfdir}/vulkan
%dir %{_sysconfdir}/vulkan/icd.d
%dir %{_sysconfdir}/vulkan/explicit_layer.d
%dir %{_sysconfdir}/vulkan/implicit_layer.d
%dir %{_datadir}/vulkan
%dir %{_datadir}/vulkan/icd.d
%dir %{_datadir}/vulkan/explicit_layer.d
%dir %{_datadir}/vulkan/implicit_layer.d
%{_libdir}/libvulkan.so.1.*.*
%ghost %{_libdir}/libvulkan.so.1

%files demos
%defattr(644,root,root,755)
%doc COPYRIGHT.txt LICENSE.txt
%attr(755,root,root) %{_bindir}/vulkan-cube
%attr(755,root,root) %{_bindir}/vulkan-smoketest
%{_datadir}/%{name}-demos

%files tools
%defattr(644,root,root,755)
%doc COPYRIGHT.txt LICENSE.txt
%doc vktrace-README.md vktrace-TODO.md
%attr(755,root,root) %{_bindir}/via
%attr(755,root,root) %{_bindir}/vkjson_info
%attr(755,root,root) %{_bindir}/vkjson_unittest
%attr(755,root,root) %{_bindir}/vulkaninfo
%ifarch %x8664
%attr(755,root,root) %{_bindir}/vkreplay
%attr(755,root,root) %{_bindir}/vktrace
%attr(755,root,root) %{_libdir}/libVkLayer_vktrace_layer.so
%{_datadir}/vulkan/explicit_layer.d/VkLayer_vktrace_layer.json
%else
%attr(755,root,root) %{_bindir}/vkreplay32
%attr(755,root,root) %{_bindir}/vktrace32
%attr(755,root,root) %{_libdir}/libVkLayer_vktrace_layer32.so
%{_datadir}/vulkan/explicit_layer.d/VkLayer_vktrace_layer32.json
%endif

%files tools-vktraceviewer
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/vktraceviewer

%files validation-layers
%defattr(644,root,root,755)
%doc COPYRIGHT.txt LICENSE.txt
%doc layers/{README.md,vk_layer_settings.txt}
%attr(755,root,root) %{_libdir}/libVkLayer_core_validation.so
%attr(755,root,root) %{_libdir}/libVkLayer_image.so
%attr(755,root,root) %{_libdir}/libVkLayer_object_tracker.so
%attr(755,root,root) %{_libdir}/libVkLayer_parameter_validation.so
%attr(755,root,root) %{_libdir}/libVkLayer_swapchain.so
%attr(755,root,root) %{_libdir}/libVkLayer_threading.so
%attr(755,root,root) %{_libdir}/libVkLayer_unique_objects.so
%attr(755,root,root) %{_libdir}/libVkLayer_utils.so
%{_datadir}/vulkan/explicit_layer.d/VkLayer_core_validation.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_image.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_object_tracker.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_parameter_validation.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_swapchain.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_threading.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_unique_objects.json

%files debug-layers
%defattr(644,root,root,755)
%doc COPYRIGHT.txt LICENSE.txt
%doc layersvt/{README.md,vk_layer_settings.txt}
%attr(755,root,root) %{_libdir}/libVkLayer_api_dump.so
%attr(755,root,root) %{_libdir}/libVkLayer_monitor.so
%attr(755,root,root) %{_libdir}/libVkLayer_screenshot.so
%attr(755,root,root) %{_libdir}/libVkLayer_utilsvt.so
%{_datadir}/vulkan/explicit_layer.d/VkLayer_api_dump.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_monitor.json
%{_datadir}/vulkan/explicit_layer.d/VkLayer_screenshot.json

%files -n vulkan-devel
%defattr(644,root,root,755)
%doc COPYRIGHT.txt LICENSE.txt README.md
%{_libdir}/libvulkan.so
%{_libdir}/libvkjson.a
%{_includedir}/vulkan
%{_includedir}/vkjson.h
%{_examplesdir}/%{name}-%{version}
