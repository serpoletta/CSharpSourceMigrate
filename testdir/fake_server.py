#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(10)
conn, addr = sock.accept()

print('connected:', addr)

diffs = "[ { methodInitializationDiff:  { methodName: 'ElectricGuitar', oldArgs: '()', newArgs: '(String brandName)', className: 'ElectricGuitar', namespace: 'default_root' } }, { namespaceDiff:  { className: 'ElectricGuitar', oldNamespace: 'default_root', newNamespace: 'Instruments' } }, { methodInitializationDiff:  { methodName: 'ElectricGuitar', oldArgs: '(int numberOfStrings)', newArgs: '(String brandName, int numberOfStrings)', className: 'ElectricGuitar', namespace: 'default_root' } }, { namespaceDiff:  { className: 'ElectricGuitar', oldNamespace: 'default_root', newNamespace: 'Instruments' } }, { namespaceDiff:  { className: 'ElectricGuitar', oldNamespace: 'default_root', newNamespace: 'Instruments' } }, { namespaceDiff:  { className: 'ElectricGuitar', oldNamespace: 'default_root', newNamespace: 'Instruments' } }, { methodSignatureDiff:  { oldName: 'ElectricGuitar', newName: 'brandName', className: 'ElectricGuitar', namespace: 'default_root' } }, { methodSignatureDiff:  { oldName: 'name', newName: 'ElectricGuitar', className: 'ElectricGuitar', namespace: 'default_root' } }, { namespaceDiff:  { className: 'Execution', oldNamespace: 'default_root', newNamespace: 'default_root' } }, { namespaceDiff:  { className: 'Execution', oldNamespace: 'default_root', newNamespace: 'default_root' } }, { methodSignatureDiff:  { oldName: 'name', newName: 'type', className: 'Instrument', namespace: 'default_root' } }, { namespaceDiff:  { className: 'Instrument', oldNamespace: 'default_root', newNamespace: 'Instruments' } }, { accessDiff:  { name: [Object], type: 'function', namespace: 'default_root', accessDiff: 'protected-func', className: 'Instrument' } }, { namespaceDiff:  { className: 'Instrument', oldNamespace: 'default_root', newNamespace: 'Instruments' } }, { namespaceDiff:  { className: 'Instrument', oldNamespace: 'default_root', newNamespace: 'Instruments' } }, { methodSignatureDiff:  { oldName: 'name', newName: 'brandName', className: 'Instrument', namespace: 'default_root' } }, { namespaceDiff:  { className: 'StringedInstrument', oldNamespace: 'default_root', newNamespace: 'Instruments' } }, { namespaceDiff:  { className: 'StringedInstrument', oldNamespace: 'default_root', newNamespace: 'Instruments' } }, { methodSignatureDiff:  { oldName: 'name', newName: 'brandName', className: 'StringedInstrument', namespace: 'default_root' } } ]"

while True:
    data = conn.recv(1024*10)
    if not data:
        break
    conn.send(diffs.encode('utf-8'))

conn.close()