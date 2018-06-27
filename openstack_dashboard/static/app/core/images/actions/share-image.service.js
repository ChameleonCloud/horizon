/**
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use self file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

(function() {
    'use strict';
  
    angular
      .module('horizon.app.core.images')
      .factory('horizon.app.core.images.actions.share-image.service', shareImageService);
  
    shareImageService.$inject = [
      '$q',
      'horizon.app.core.openstack-service-api.glance',
      'horizon.app.core.openstack-service-api.userSession',
      'horizon.app.core.images.non_bootable_image_types',
      'horizon.dashboard.project.workflow.launch-instance.modal.service',
      'horizon.framework.util.q.extensions',
      'horizon.app.core.openstack-service-api.policy'
    ];
  
    /**
     * @ngDoc factory
     * @name horizon.app.core.images.actions.shareImageService
     * @param {Object} $q
     * @param {Object} nonBootableImageTypes
     * @param {Object} launchInstanceModal
     * @param {Object} $qExtensions
     * @Description
     * Brings up the Launch Instance for image modal.
     * On submit, launch the instance for the Image.
     * On cancel, do nothing.
     *
     * @returns {Object} The service
     */
    function shareImageService(
      $q,
      glance,
      userSessionService,
      nonBootableImageTypes,
      launchInstanceModal,
      $qExtensions
    ) {
      var service = {
        perform: perform,
        allowed: allowed
      };
      var modifyImagePolicyCheck, scope;
  
      return service;

      function initScope($scope) {
        scope = $scope;
        $scope.$on(events.IMAGE_METADATA_CHANGED, onMetadataChange);
        modifyImagePolicyCheck = policy.ifAllowed({rules: [['image', 'modify_image']]});
      }

      function allowed(image) {
        return $q.all([
          modifyImagePolicyCheck,
          userSessionService.isCurrentProject(image.owner),
          isActive(image)
        ]);
      }

      //////////////
  
      function perform(image) {
        // Previous uses of this relocated the display using the successUrl;
        // in this case we leave the post-action behavior up to the result
        // handler.
        // return launchInstanceModal.open({
        //   'imageId': image.id
        // });
        console.log(image);
        console.log(userSessionService.isCurrentProject(image.owner));
        var params = '?name=' + escape(image.name);
        params += '&short_description=' + escape(image.properties.description === undefined ? '' : image.properties.description);
        var region = getCookie('services_region');
        //var region = userSessionService.get().then(function(userSession){return userSession.services_region;});
        if('region'.indexOf('@tacc') != -1){
          params += '&chi_tacc_appliance_id=' + escape(image.id);
        } else {
          params += '&chi_uc_appliance_id=' + escape(image.id);
        }
        if(window.location.hostname.indexOf('dev.chameleon') > -1 || window.location.port != 443){
          return window.open('https://dev.chameleon.tacc.utexas.edu/appliances/create' + params);
        } else {
          return window.open('https://www.chameleoncloud.org/appliances/create' + params);
        }
      }

      function getCookie(cname) {
        var name = cname + "=";
        var decodedCookie = decodeURIComponent(document.cookie);
        var ca = decodedCookie.split(';');
        for(var i = 0; i <ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }
  
      function isActive(image) {
        return $qExtensions.booleanAsPromise(image.status === 'active');
      }
  
      function isBootable(image) {
        return $qExtensions.booleanAsPromise(
          nonBootableImageTypes.indexOf(image.container_format) < 0
        );
      }
  
    } // end of shareImageService
  })(); // end of IIFE
  