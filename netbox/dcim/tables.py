import django_tables2 as tables
from django_tables2.utils import Accessor

from utilities.tables import BaseTable, ToggleColumn

from .models import (
    ConsolePort, ConsolePortTemplate, ConsoleServerPortTemplate, Device, DeviceBayTemplate, DeviceRole, DeviceType,
    Interface, InterfaceTemplate, Manufacturer, Platform, PowerOutletTemplate, PowerPort, PowerPortTemplate, Rack,
    RackGroup, RackReservation, Region, Site,
)


REGION_LINK = """
{% if record.get_children %}
    <span style="padding-left: {{ record.get_ancestors|length }}0px "><i class="fa fa-caret-right"></i>
{% else %}
    <span style="padding-left: {{ record.get_ancestors|length }}9px">
{% endif %}
    <a href="{% url 'dcim:site_list' %}?region={{ record.slug }}">{{ record.name }}</a>
</span>
"""

SITE_REGION_LINK = """
{% if record.region %}
    <a href="{% url 'dcim:site_list' %}?region={{ record.region.slug }}">{{ record.region }}</a>
{% else %}
    &mdash;
{% endif %}
"""

COLOR_LABEL = """
<label class="label" style="background-color: #{{ record.color }}">{{ record }}</label>
"""

DEVICE_LINK = """
<a href="{% url 'dcim:device' pk=record.pk %}">
    {{ record.name|default:'<span class="label label-info">Unnamed device</span>' }}
</a>
"""

REGION_ACTIONS = """
{% if perms.dcim.change_region %}
    <a href="{% url 'dcim:region_edit' pk=record.pk %}" class="btn btn-xs btn-warning"><i class="glyphicon glyphicon-pencil" aria-hidden="true"></i></a>
{% endif %}
"""

RACKGROUP_ACTIONS = """
{% if perms.dcim.change_rackgroup %}
    <a href="{% url 'dcim:rackgroup_edit' pk=record.pk %}" class="btn btn-xs btn-warning"><i class="glyphicon glyphicon-pencil" aria-hidden="true"></i></a>
{% endif %}
"""

RACKROLE_ACTIONS = """
{% if perms.dcim.change_rackrole %}
    <a href="{% url 'dcim:rackrole_edit' pk=record.pk %}" class="btn btn-xs btn-warning"><i class="glyphicon glyphicon-pencil" aria-hidden="true"></i></a>
{% endif %}
"""

RACK_ROLE = """
{% if record.role %}
    <label class="label" style="background-color: #{{ record.role.color }}">{{ value }}</label>
{% else %}
    &mdash;
{% endif %}
"""

RACKRESERVATION_ACTIONS = """
{% if perms.dcim.change_rackreservation %}
    <a href="{% url 'dcim:rackreservation_edit' pk=record.pk %}" class="btn btn-xs btn-warning"><i class="glyphicon glyphicon-pencil" aria-hidden="true"></i></a>
{% endif %}
"""

DEVICEROLE_ACTIONS = """
{% if perms.dcim.change_devicerole %}
    <a href="{% url 'dcim:devicerole_edit' slug=record.slug %}" class="btn btn-xs btn-warning"><i class="glyphicon glyphicon-pencil" aria-hidden="true"></i></a>
{% endif %}
"""

MANUFACTURER_ACTIONS = """
{% if perms.dcim.change_manufacturer %}
    <a href="{% url 'dcim:manufacturer_edit' slug=record.slug %}" class="btn btn-xs btn-warning"><i class="glyphicon glyphicon-pencil" aria-hidden="true"></i></a>
{% endif %}
"""

PLATFORM_ACTIONS = """
{% if perms.dcim.change_platform %}
    <a href="{% url 'dcim:platform_edit' slug=record.slug %}" class="btn btn-xs btn-warning"><i class="glyphicon glyphicon-pencil" aria-hidden="true"></i></a>
{% endif %}
"""

DEVICE_ROLE = """
<label class="label" style="background-color: #{{ record.device_role.color }}">{{ value }}</label>
"""

STATUS_ICON = """
{% if record.status %}
    <span class="glyphicon glyphicon-ok-sign text-success" title="Active" aria-hidden="true"></span>
{% else %}
    <span class="glyphicon glyphicon-minus-sign text-danger" title="Offline" aria-hidden="true"></span>
{% endif %}
"""

DEVICE_PRIMARY_IP = """
{{ record.primary_ip6.address.ip|default:"" }}
{% if record.primary_ip6 and record.primary_ip4 %}<br />{% endif %}
{{ record.primary_ip4.address.ip|default:"" }}
"""

SUBDEVICE_ROLE_TEMPLATE = """
{% if record.subdevice_role == True %}Parent{% elif record.subdevice_role == False %}Child{% else %}&mdash;{% endif %}
"""

UTILIZATION_GRAPH = """
{% load helpers %}
{% utilization_graph value %}
"""


#
# Regions
#

class RegionTable(BaseTable):
    pk = ToggleColumn()
    name = tables.TemplateColumn(template_code=REGION_LINK, orderable=False)
    site_count = tables.Column(verbose_name='Sites')
    slug = tables.Column(verbose_name='Slug')
    actions = tables.TemplateColumn(
        template_code=REGION_ACTIONS,
        attrs={'td': {'class': 'text-right'}},
        verbose_name=''
    )

    class Meta(BaseTable.Meta):
        model = Region
        fields = ('pk', 'name', 'site_count', 'slug', 'actions')


#
# Sites
#

class SiteTable(BaseTable):
    pk = ToggleColumn()
    name = tables.LinkColumn('dcim:site', args=[Accessor('slug')], verbose_name='Name')
    facility = tables.Column(verbose_name='Facility')
    region = tables.TemplateColumn(template_code=SITE_REGION_LINK, verbose_name='Region')
    tenant = tables.LinkColumn('tenancy:tenant', args=[Accessor('tenant.slug')], verbose_name='Tenant')
    asn = tables.Column(verbose_name='ASN')
    rack_count = tables.Column(accessor=Accessor('count_racks'), orderable=False, verbose_name='Racks')
    device_count = tables.Column(accessor=Accessor('count_devices'), orderable=False, verbose_name='Devices')
    prefix_count = tables.Column(accessor=Accessor('count_prefixes'), orderable=False, verbose_name='Prefixes')
    vlan_count = tables.Column(accessor=Accessor('count_vlans'), orderable=False, verbose_name='VLANs')
    circuit_count = tables.Column(accessor=Accessor('count_circuits'), orderable=False, verbose_name='Circuits')

    class Meta(BaseTable.Meta):
        model = Site
        fields = (
            'pk', 'name', 'facility', 'region', 'tenant', 'asn', 'rack_count', 'device_count', 'prefix_count',
            'vlan_count', 'circuit_count',
        )


#
# Rack groups
#

class RackGroupTable(BaseTable):
    pk = ToggleColumn()
    name = tables.LinkColumn(verbose_name='Name')
    site = tables.LinkColumn('dcim:site', args=[Accessor('site.slug')], verbose_name='Site')
    rack_count = tables.Column(verbose_name='Racks')
    slug = tables.Column(verbose_name='Slug')
    actions = tables.TemplateColumn(template_code=RACKGROUP_ACTIONS, attrs={'td': {'class': 'text-right'}},
                                    verbose_name='')

    class Meta(BaseTable.Meta):
        model = RackGroup
        fields = ('pk', 'name', 'site', 'rack_count', 'slug', 'actions')


#
# Rack roles
#

class RackRoleTable(BaseTable):
    pk = ToggleColumn()
    name = tables.LinkColumn(verbose_name='Name')
    rack_count = tables.Column(verbose_name='Racks')
    color = tables.TemplateColumn(COLOR_LABEL, verbose_name='Color')
    slug = tables.Column(verbose_name='Slug')
    actions = tables.TemplateColumn(template_code=RACKROLE_ACTIONS, attrs={'td': {'class': 'text-right'}},
                                    verbose_name='')

    class Meta(BaseTable.Meta):
        model = RackGroup
        fields = ('pk', 'name', 'rack_count', 'color', 'slug', 'actions')


#
# Racks
#

class RackTable(BaseTable):
    pk = ToggleColumn()
    name = tables.LinkColumn('dcim:rack', args=[Accessor('pk')], verbose_name='Name')
    site = tables.LinkColumn('dcim:site', args=[Accessor('site.slug')], verbose_name='Site')
    group = tables.Column(accessor=Accessor('group.name'), verbose_name='Group')
    facility_id = tables.Column(verbose_name='Facility ID')
    tenant = tables.LinkColumn('tenancy:tenant', args=[Accessor('tenant.slug')], verbose_name='Tenant')
    role = tables.TemplateColumn(RACK_ROLE, verbose_name='Role')
    u_height = tables.TemplateColumn("{{ record.u_height }}U", verbose_name='Height')
    devices = tables.Column(accessor=Accessor('device_count'), verbose_name='Devices')
    get_utilization = tables.TemplateColumn(UTILIZATION_GRAPH, orderable=False, verbose_name='Utilization')

    class Meta(BaseTable.Meta):
        model = Rack
        fields = ('pk', 'name', 'site', 'group', 'facility_id', 'tenant', 'role', 'u_height', 'devices',
                  'get_utilization')


class RackImportTable(BaseTable):
    name = tables.LinkColumn('dcim:rack', args=[Accessor('pk')], verbose_name='Name')
    site = tables.LinkColumn('dcim:site', args=[Accessor('site.slug')], verbose_name='Site')
    group = tables.Column(accessor=Accessor('group.name'), verbose_name='Group')
    facility_id = tables.Column(verbose_name='Facility ID')
    tenant = tables.LinkColumn('tenancy:tenant', args=[Accessor('tenant.slug')], verbose_name='Tenant')
    u_height = tables.Column(verbose_name='Height (U)')

    class Meta(BaseTable.Meta):
        model = Rack
        fields = ('site', 'group', 'name', 'facility_id', 'tenant', 'u_height')


#
# Rack reservations
#

class RackReservationTable(BaseTable):
    pk = ToggleColumn()
    rack = tables.LinkColumn('dcim:rack', args=[Accessor('rack.pk')])
    unit_list = tables.Column(orderable=False, verbose_name='Units')
    actions = tables.TemplateColumn(
        template_code=RACKRESERVATION_ACTIONS, attrs={'td': {'class': 'text-right'}}, verbose_name=''
    )

    class Meta(BaseTable.Meta):
        model = RackReservation
        fields = ('pk', 'rack', 'unit_list', 'user', 'created', 'description', 'actions')


#
# Manufacturers
#

class ManufacturerTable(BaseTable):
    pk = ToggleColumn()
    name = tables.LinkColumn(verbose_name='Name')
    devicetype_count = tables.Column(verbose_name='Device Types')
    slug = tables.Column(verbose_name='Slug')
    actions = tables.TemplateColumn(template_code=MANUFACTURER_ACTIONS, attrs={'td': {'class': 'text-right'}},
                                    verbose_name='')

    class Meta(BaseTable.Meta):
        model = Manufacturer
        fields = ('pk', 'name', 'devicetype_count', 'slug', 'actions')


#
# Device types
#

class DeviceTypeTable(BaseTable):
    pk = ToggleColumn()
    manufacturer = tables.Column(verbose_name='Manufacturer')
    model = tables.LinkColumn('dcim:devicetype', args=[Accessor('pk')], verbose_name='Device Type')
    part_number = tables.Column(verbose_name='Part Number')
    is_full_depth = tables.BooleanColumn(verbose_name='Full Depth')
    is_console_server = tables.BooleanColumn(verbose_name='CS')
    is_pdu = tables.BooleanColumn(verbose_name='PDU')
    is_network_device = tables.BooleanColumn(verbose_name='Net')
    subdevice_role = tables.TemplateColumn(SUBDEVICE_ROLE_TEMPLATE, verbose_name='Subdevice Role')
    instance_count = tables.Column(verbose_name='Instances')

    class Meta(BaseTable.Meta):
        model = DeviceType
        fields = (
            'pk', 'model', 'manufacturer', 'part_number', 'u_height', 'is_full_depth', 'is_console_server', 'is_pdu',
            'is_network_device', 'subdevice_role', 'instance_count'
        )


#
# Device type components
#

class ConsolePortTemplateTable(BaseTable):
    pk = ToggleColumn()

    class Meta(BaseTable.Meta):
        model = ConsolePortTemplate
        fields = ('pk', 'name')
        empty_text = "None"
        show_header = False


class ConsoleServerPortTemplateTable(BaseTable):
    pk = ToggleColumn()

    class Meta(BaseTable.Meta):
        model = ConsoleServerPortTemplate
        fields = ('pk', 'name')
        empty_text = "None"
        show_header = False


class PowerPortTemplateTable(BaseTable):
    pk = ToggleColumn()

    class Meta(BaseTable.Meta):
        model = PowerPortTemplate
        fields = ('pk', 'name')
        empty_text = "None"
        show_header = False


class PowerOutletTemplateTable(BaseTable):
    pk = ToggleColumn()

    class Meta(BaseTable.Meta):
        model = PowerOutletTemplate
        fields = ('pk', 'name')
        empty_text = "None"
        show_header = False


class InterfaceTemplateTable(BaseTable):
    pk = ToggleColumn()

    class Meta(BaseTable.Meta):
        model = InterfaceTemplate
        fields = ('pk', 'name', 'form_factor')
        empty_text = "None"
        show_header = False


class DeviceBayTemplateTable(BaseTable):
    pk = ToggleColumn()

    class Meta(BaseTable.Meta):
        model = DeviceBayTemplate
        fields = ('pk', 'name')
        empty_text = "None"
        show_header = False


#
# Device roles
#

class DeviceRoleTable(BaseTable):
    pk = ToggleColumn()
    name = tables.LinkColumn(verbose_name='Name')
    device_count = tables.Column(verbose_name='Devices')
    color = tables.TemplateColumn(COLOR_LABEL, verbose_name='Color')
    slug = tables.Column(verbose_name='Slug')
    actions = tables.TemplateColumn(template_code=DEVICEROLE_ACTIONS, attrs={'td': {'class': 'text-right'}},
                                    verbose_name='')

    class Meta(BaseTable.Meta):
        model = DeviceRole
        fields = ('pk', 'name', 'device_count', 'color', 'slug', 'actions')


#
# Platforms
#

class PlatformTable(BaseTable):
    pk = ToggleColumn()
    name = tables.LinkColumn(verbose_name='Name')
    device_count = tables.Column(verbose_name='Devices')
    slug = tables.Column(verbose_name='Slug')
    actions = tables.TemplateColumn(template_code=PLATFORM_ACTIONS, attrs={'td': {'class': 'text-right'}},
                                    verbose_name='')

    class Meta(BaseTable.Meta):
        model = Platform
        fields = ('pk', 'name', 'device_count', 'slug', 'actions')


#
# Devices
#

class DeviceTable(BaseTable):
    pk = ToggleColumn()
    status = tables.TemplateColumn(template_code=STATUS_ICON, verbose_name='')
    name = tables.TemplateColumn(template_code=DEVICE_LINK, verbose_name='Name')
    tenant = tables.LinkColumn('tenancy:tenant', args=[Accessor('tenant.slug')], verbose_name='Tenant')
    site = tables.LinkColumn('dcim:site', args=[Accessor('site.slug')], verbose_name='Site')
    rack = tables.LinkColumn('dcim:rack', args=[Accessor('rack.pk')], verbose_name='Rack')
    device_role = tables.TemplateColumn(DEVICE_ROLE, verbose_name='Role')
    device_type = tables.LinkColumn('dcim:devicetype', args=[Accessor('device_type.pk')], verbose_name='Type',
                                    text=lambda record: record.device_type.full_name)
    primary_ip = tables.TemplateColumn(orderable=False, verbose_name='IP Address',
                                       template_code=DEVICE_PRIMARY_IP)

    class Meta(BaseTable.Meta):
        model = Device
        fields = ('pk', 'name', 'status', 'tenant', 'site', 'rack', 'device_role', 'device_type', 'primary_ip')


class DeviceImportTable(BaseTable):
    name = tables.TemplateColumn(template_code=DEVICE_LINK, verbose_name='Name')
    tenant = tables.LinkColumn('tenancy:tenant', args=[Accessor('tenant.slug')], verbose_name='Tenant')
    site = tables.LinkColumn('dcim:site', args=[Accessor('site.slug')], verbose_name='Site')
    rack = tables.LinkColumn('dcim:rack', args=[Accessor('rack.pk')], verbose_name='Rack')
    position = tables.Column(verbose_name='Position')
    device_role = tables.Column(verbose_name='Role')
    device_type = tables.Column(verbose_name='Type')

    class Meta(BaseTable.Meta):
        model = Device
        fields = ('name', 'tenant', 'site', 'rack', 'position', 'device_role', 'device_type')
        empty_text = False


#
# Device connections
#

class ConsoleConnectionTable(BaseTable):
    console_server = tables.LinkColumn('dcim:device', accessor=Accessor('cs_port.device'),
                                       args=[Accessor('cs_port.device.pk')], verbose_name='Console server')
    cs_port = tables.Column(verbose_name='Port')
    device = tables.LinkColumn('dcim:device', args=[Accessor('device.pk')], verbose_name='Device')
    name = tables.Column(verbose_name='Console port')

    class Meta(BaseTable.Meta):
        model = ConsolePort
        fields = ('console_server', 'cs_port', 'device', 'name')


class PowerConnectionTable(BaseTable):
    pdu = tables.LinkColumn('dcim:device', accessor=Accessor('power_outlet.device'),
                            args=[Accessor('power_outlet.device.pk')], verbose_name='PDU')
    power_outlet = tables.Column(verbose_name='Outlet')
    device = tables.LinkColumn('dcim:device', args=[Accessor('device.pk')], verbose_name='Device')
    name = tables.Column(verbose_name='Power Port')

    class Meta(BaseTable.Meta):
        model = PowerPort
        fields = ('pdu', 'power_outlet', 'device', 'name')


class InterfaceConnectionTable(BaseTable):
    device_a = tables.LinkColumn('dcim:device', accessor=Accessor('interface_a.device'),
                                 args=[Accessor('interface_a.device.pk')], verbose_name='Device A')
    interface_a = tables.Column(verbose_name='Interface A')
    device_b = tables.LinkColumn('dcim:device', accessor=Accessor('interface_b.device'),
                                 args=[Accessor('interface_b.device.pk')], verbose_name='Device B')
    interface_b = tables.Column(verbose_name='Interface B')

    class Meta(BaseTable.Meta):
        model = Interface
        fields = ('device_a', 'interface_a', 'device_b', 'interface_b')
