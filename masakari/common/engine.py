#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright(c) 2015 Nippon Telegraph and Telephone Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from oslo_config import cfg
engine_default_group = cfg.OptGroup(name='engine_default',
                                    title="Default Options for Masakari")
engine_wsgi_group = cfg.OptGroup(name='engine_wsgi',
                                 title='wsgi options for engine(ToBeRemoved)')
engine_db_group = cfg.OptGroup(name='engine_db',
                               title='db options for engine')

engine_log_group = cfg.OptGroup(name='engine_log',
                                title='log settings for engine')
engine_nova_group = cfg.OptGroup(name='engine_nova',
                                 title='settings for novaclient')

# TODO(samp): Remove this with new notification model
engine_wsgi_opt = cfg.IntOpt('server_port',
                             default=15868,
                             help='wsgi server port for masakari engine')

# TODO(samp): Remove this with oslo.db settings
engine_db_opt = [
    cfg.StrOpt('drivername',
               default="sqlite",
               help='db driver for masakari engine'),
    cfg.StrOpt('host',
               default= None,
               help='db host for masakari engine'),
    cfg.StrOpt('name',
               default='vm_ha',
               help='db name for masakari engine'),
    cfg.StrOpt('user',
               default='root',
               help='user name for access the db'),
    cfg.StrOpt('password',
               default='password',
               help='password to access the db'),
    cfg.StrOpt('charset',
               default='utf8',
               help='Char set for db'),
    cfg.IntOpt('lock_retry_max_cnt',
               default=6,
               help='Maxmum retry count when db locked'),
    cfg.IntOpt('innodb_lock_wait_timeout',
               default=50,
               help='Wait time for innodb lock')
]

# TODO(samp): Remove this with default log settings
engine_log_opt = [
    cfg.StrOpt('log_level',
               default='info',
               help='Log level'),
    cfg.StrOpt('log_file',
               default='/var/log/masakari/masakari-controller.log',
               help="Path for log file")
]

# TODO(samp): Move this to [Default] section

engine_recovery_opt = [
    cfg.IntOpt('interval_to_be_retry',
               default=300,
               help='Retry interval'),
    cfg.IntOpt('max_retry_cnt',
               default=3,
               help='Max retry count'),
    cfg.IntOpt('semaphore_multiplicity',
               default=5,
               help='semaphore multiplicity'),
    cfg.IntOpt('notification_time_difference',
               default=240,
               help='notification time difference'),
    cfg.IntOpt('node_err_wait',
               default=180,
               help='waiting time for node error'),
    cfg.IntOpt('api_max_retry_cnt',
               default=3,
               help='api_max_retry_cnt'),
    cfg.IntOpt('api_retry_interval',
               default=10,
               help='api_retry_interval'),
    cfg.IntOpt('recovery_max_retry_cnt',
               default=6,
               help='recovery_max_retry_cnt'),
    cfg.IntOpt('recovery_retry_interval',
               default=10,
               help='recovery_retry_interval'),
    cfg.IntOpt('api_check_interval',
               default=1,
               help='api_check_interval'),
    cfg.IntOpt('api_check_max_cnt',
               default=30,
               help='api_check_max_cnt'),
    cfg.IntOpt('notification_expiration_sec',
               default=900,
               help='notification_expiration_sec')
]

# TODO(samp): Remove this with [keystone_authtoken]
engine_nova_opt = [
    cfg.StrOpt('domain',
               default='Default',
               help='Keystone Domain'),
    cfg.StrOpt('admin_user',
               default='admin',
               help='Admin user name'),
    cfg.StrOpt('admin_password',
               default='password',
               help='Password for admin user'),
    cfg.StrOpt('auth_url',
               default='http://192.168.50.10:5000',
               help='keystone auth url'),
    cfg.StrOpt('project_name',
               default='demo',
               help='project name')
    ]

# TODO(samp): Move this to [Default] section
engine_vmha_data_manage_opt = cfg.IntOpt('period',
                                         default=30,
                                         help='period')


def register_opts(conf):
    conf.register_opts(engine_recovery_opt, group=engine_default_group)
    conf.register_opts(engine_vmha_data_manage_opt, group=engine_default_group)
    conf.register_opts(engine_wsgi_opt, group=engine_wsgi_group)
    conf.register_opts(engine_db_opt, group=engine_db_group)
    conf.register_opts(engine_log_opt, group=engine_log_group)
    conf.register_opts(engine_nova_opt, group=engine_nova_group)


def list_opts():
    ops_dict = {
        engine_default_group: engine_recovery_opt,
        engine_default_group: engine_vmha_data_manage_opt,
        engine_wsgi_group: engine_wsgi_opt,
        engine_db_group: engine_db_opt,
        engine_log_group: engine_log_opt,
        engine_nova_group: engine_nova_opt
    }
    return ops_dict
