/*
 *    (c) Copyright 2015 Hewlett-Packard Development Company, L.P.
 *
 * Licensed under the Apache License, Version 2.0 (the 'License');
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an 'AS IS' BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
(function() {
  'use strict';

  describe('horizon.dashboard.project.workflow.launch-instance.workflow tests', function () {
    var createWorkflow, launchInstanceWorkflow, stepPolicy;

    beforeEach(module('horizon.app.core'));
    beforeEach(module('horizon.framework.util'));
    beforeEach(module('horizon.framework.conf'));
    beforeEach(module('horizon.framework.widgets.toast'));
    beforeEach(module('horizon.dashboard.project'));

    beforeEach(inject(function ($injector) {
      createWorkflow = $injector.get(
        'horizon.dashboard.project.workflow.launch-instance.workflow'
      );
      stepPolicy = $injector.get('horizon.dashboard.project.workflow.launch-instance.step-policy');
      launchInstanceWorkflow = createWorkflow('baremetal');
    }));

    it('should be defined', function () {
      expect(launchInstanceWorkflow).toBeDefined();
    });

    it('should have a title property', function () {
      expect(launchInstanceWorkflow.title).toBeDefined();
    });

    it('should have 11 steps defined', function () {
      expect(launchInstanceWorkflow.steps).toBeDefined();
      expect(launchInstanceWorkflow.steps.length).toBe(11);

      var forms = [
        'launchInstanceDetailsForm',
        'launchInstanceSourceForm',
        'launchInstanceFlavorForm',
        'launchInstanceNetworkForm',
        'launchInstanceNetworkPortForm',
        'launchInstanceAccessAndSecurityForm',
        'launchInstanceKeypairForm',
        'launchInstanceConfigurationForm',
        'launchInstanceServerGroupsForm',
        'launchInstanceSchedulerHintsForm',
        'launchInstanceMetadataForm'
      ];

      forms.forEach(function(expectedForm, idx) {
        expect(launchInstanceWorkflow.steps[idx].formName).toBe(expectedForm);
      });
    });

    it('specifies that the network step requires the network service type', function() {
      expect(launchInstanceWorkflow.steps[3].requiredServiceTypes).toEqual(['network']);
    });

    it('specifies that the network port step requires the network service type', function() {
      expect(launchInstanceWorkflow.steps[4].requiredServiceTypes).toEqual(['network']);
    });

    it('has a policy rule for the server groups step', function() {
      expect(launchInstanceWorkflow.steps[8].policy).toEqual(stepPolicy.serverGroups);
    });

    it('has a policy rule for the scheduler hints step', function() {
      expect(launchInstanceWorkflow.steps[9].policy).toEqual(stepPolicy.schedulerHints);
    });

    it('CHI: collapses all but four steps behind the advanced toggle for baremetal', function() {
      expect(launchInstanceWorkflow.advanced).toEqual({showButton: true, showTabs: false});
      expect(launchInstanceWorkflow.steps
        .filter(function(step) { return !step.isAdvanced; })
        .map(function(step) { return step.id; }))
        .toEqual(['details', 'source', 'networks', 'keypair']);
    });

    it('CHI: gives virtual every tab and no advanced toggle', function() {
      var virtual = createWorkflow('virtual');

      expect(virtual.advanced).toEqual({showButton: false, showTabs: true});
      expect(virtual.steps.some(function(step) { return step.isAdvanced; })).toBe(false);
      expect(virtual.steps.length).toBe(launchInstanceWorkflow.steps.length);
    });

    it('CHI: does not let one instance type leak into the next', function() {
      createWorkflow('virtual');

      expect(createWorkflow('baremetal').advanced)
        .toEqual({showButton: true, showTabs: false});
    });

    it('CHI: treats any non-baremetal type as the flat upstream layout', function() {
      expect(createWorkflow('upstream').advanced)
        .toEqual({showButton: false, showTabs: true});
    });

  });

})();
