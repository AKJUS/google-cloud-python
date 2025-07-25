#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
#
import argparse
import os
import libcst as cst
import pathlib
import sys
from typing import (Any, Callable, Dict, List, Sequence, Tuple)


def partition(
    predicate: Callable[[Any], bool],
    iterator: Sequence[Any]
) -> Tuple[List[Any], List[Any]]:
    """A stable, out-of-place partition."""
    results = ([], [])

    for i in iterator:
        results[int(predicate(i))].append(i)

    # Returns trueList, falseList
    return results[1], results[0]


class retailCallTransformer(cst.CSTTransformer):
    CTRL_PARAMS: Tuple[str] = ('retry', 'timeout', 'metadata')
    METHOD_TO_PARAMS: Dict[str, Tuple[str]] = {
        'accept_terms': ('project', ),
        'add_catalog_attribute': ('attributes_config', 'catalog_attribute', ),
        'add_control': ('serving_config', 'control_id', ),
        'add_fulfillment_places': ('product', 'type_', 'place_ids', 'add_time', 'allow_missing', ),
        'add_local_inventories': ('product', 'local_inventories', 'add_mask', 'add_time', 'allow_missing', ),
        'batch_remove_catalog_attributes': ('attributes_config', 'attribute_keys', ),
        'batch_update_generative_question_configs': ('requests', 'parent', ),
        'collect_user_event': ('parent', 'user_event', 'prebuilt_rule', 'uri', 'ets', 'raw_json', ),
        'complete_query': ('catalog', 'query', 'visitor_id', 'language_codes', 'device_type', 'dataset', 'max_suggestions', 'enable_attribute_suggestions', 'entity', ),
        'conversational_search': ('placement', 'branch', 'visitor_id', 'query', 'page_categories', 'conversation_id', 'search_params', 'user_info', 'conversational_filtering_spec', 'user_labels', 'safety_settings', ),
        'create_control': ('parent', 'control', 'control_id', ),
        'create_merchant_center_account_link': ('parent', 'merchant_center_account_link', ),
        'create_model': ('parent', 'model', 'dry_run', ),
        'create_product': ('parent', 'product', 'product_id', ),
        'create_serving_config': ('parent', 'serving_config', 'serving_config_id', ),
        'delete_control': ('name', ),
        'delete_merchant_center_account_link': ('name', ),
        'delete_model': ('name', ),
        'delete_product': ('name', 'force', ),
        'delete_serving_config': ('name', ),
        'enroll_solution': ('project', 'solution', ),
        'export_analytics_metrics': ('catalog', 'output_config', 'filter', ),
        'export_products': ('parent', 'output_config', 'filter', ),
        'export_user_events': ('parent', 'output_config', 'filter', ),
        'get_alert_config': ('name', ),
        'get_attributes_config': ('name', ),
        'get_branch': ('name', 'view', ),
        'get_completion_config': ('name', ),
        'get_control': ('name', ),
        'get_default_branch': ('catalog', ),
        'get_generative_questions_feature_config': ('catalog', ),
        'get_logging_config': ('name', ),
        'get_model': ('name', ),
        'get_product': ('name', ),
        'get_project': ('name', ),
        'get_serving_config': ('name', ),
        'import_completion_data': ('parent', 'input_config', 'notification_pubsub_topic', ),
        'import_products': ('parent', 'input_config', 'request_id', 'errors_config', 'update_mask', 'reconciliation_mode', 'notification_pubsub_topic', 'skip_default_branch_protection', ),
        'import_user_events': ('parent', 'input_config', 'errors_config', ),
        'list_branches': ('parent', 'view', ),
        'list_catalogs': ('parent', 'page_size', 'page_token', ),
        'list_controls': ('parent', 'page_size', 'page_token', 'filter', ),
        'list_enrolled_solutions': ('parent', ),
        'list_generative_question_configs': ('parent', ),
        'list_merchant_center_account_links': ('parent', ),
        'list_models': ('parent', 'page_size', 'page_token', ),
        'list_products': ('parent', 'page_size', 'page_token', 'filter', 'read_mask', 'require_total_size', ),
        'list_serving_configs': ('parent', 'page_size', 'page_token', ),
        'pause_model': ('name', ),
        'predict': ('placement', 'user_event', 'page_size', 'page_token', 'filter', 'validate_only', 'params', 'labels', ),
        'purge_products': ('parent', 'filter', 'force', ),
        'purge_user_events': ('parent', 'filter', 'force', ),
        'rejoin_user_events': ('parent', 'user_event_rejoin_scope', ),
        'remove_catalog_attribute': ('attributes_config', 'key', ),
        'remove_control': ('serving_config', 'control_id', ),
        'remove_fulfillment_places': ('product', 'type_', 'place_ids', 'remove_time', 'allow_missing', ),
        'remove_local_inventories': ('product', 'place_ids', 'remove_time', 'allow_missing', ),
        'replace_catalog_attribute': ('attributes_config', 'catalog_attribute', 'update_mask', ),
        'resume_model': ('name', ),
        'search': ('placement', 'visitor_id', 'branch', 'query', 'user_info', 'page_size', 'page_token', 'offset', 'filter', 'canonical_filter', 'order_by', 'facet_specs', 'dynamic_facet_spec', 'boost_spec', 'query_expansion_spec', 'relevance_threshold', 'variant_rollup_keys', 'experiment_id', 'page_categories', 'search_mode', 'personalization_spec', 'labels', 'spell_correction_spec', 'entity', 'conversational_search_spec', 'tile_navigation_spec', 'language_code', 'region_code', 'place_id', 'user_attributes', ),
        'set_default_branch': ('catalog', 'branch_id', 'note', 'force', ),
        'set_inventory': ('inventory', 'set_mask', 'set_time', 'allow_missing', ),
        'tune_model': ('name', ),
        'update_alert_config': ('alert_config', 'update_mask', ),
        'update_attributes_config': ('attributes_config', 'update_mask', ),
        'update_catalog': ('catalog', 'update_mask', ),
        'update_completion_config': ('completion_config', 'update_mask', ),
        'update_control': ('control', 'update_mask', ),
        'update_generative_question_config': ('generative_question_config', 'update_mask', ),
        'update_generative_questions_feature_config': ('generative_questions_feature_config', 'update_mask', ),
        'update_logging_config': ('logging_config', 'update_mask', ),
        'update_model': ('model', 'update_mask', ),
        'update_product': ('product', 'update_mask', 'allow_missing', ),
        'update_serving_config': ('serving_config', 'update_mask', ),
        'write_user_event': ('parent', 'user_event', 'write_async', ),
    }

    def leave_Call(self, original: cst.Call, updated: cst.Call) -> cst.CSTNode:
        try:
            key = original.func.attr.value
            kword_params = self.METHOD_TO_PARAMS[key]
        except (AttributeError, KeyError):
            # Either not a method from the API or too convoluted to be sure.
            return updated

        # If the existing code is valid, keyword args come after positional args.
        # Therefore, all positional args must map to the first parameters.
        args, kwargs = partition(lambda a: not bool(a.keyword), updated.args)
        if any(k.keyword.value == "request" for k in kwargs):
            # We've already fixed this file, don't fix it again.
            return updated

        kwargs, ctrl_kwargs = partition(
            lambda a: a.keyword.value not in self.CTRL_PARAMS,
            kwargs
        )

        args, ctrl_args = args[:len(kword_params)], args[len(kword_params):]
        ctrl_kwargs.extend(cst.Arg(value=a.value, keyword=cst.Name(value=ctrl))
                           for a, ctrl in zip(ctrl_args, self.CTRL_PARAMS))

        request_arg = cst.Arg(
            value=cst.Dict([
                cst.DictElement(
                    cst.SimpleString("'{}'".format(name)),
cst.Element(value=arg.value)
                )
                # Note: the args + kwargs looks silly, but keep in mind that
                # the control parameters had to be stripped out, and that
                # those could have been passed positionally or by keyword.
                for name, arg in zip(kword_params, args + kwargs)]),
            keyword=cst.Name("request")
        )

        return updated.with_changes(
            args=[request_arg] + ctrl_kwargs
        )


def fix_files(
    in_dir: pathlib.Path,
    out_dir: pathlib.Path,
    *,
    transformer=retailCallTransformer(),
):
    """Duplicate the input dir to the output dir, fixing file method calls.

    Preconditions:
    * in_dir is a real directory
    * out_dir is a real, empty directory
    """
    pyfile_gen = (
        pathlib.Path(os.path.join(root, f))
        for root, _, files in os.walk(in_dir)
        for f in files if os.path.splitext(f)[1] == ".py"
    )

    for fpath in pyfile_gen:
        with open(fpath, 'r') as f:
            src = f.read()

        # Parse the code and insert method call fixes.
        tree = cst.parse_module(src)
        updated = tree.visit(transformer)

        # Create the path and directory structure for the new file.
        updated_path = out_dir.joinpath(fpath.relative_to(in_dir))
        updated_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate the updated source file at the corresponding path.
        with open(updated_path, 'w') as f:
            f.write(updated.code)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""Fix up source that uses the retail client library.

The existing sources are NOT overwritten but are copied to output_dir with changes made.

Note: This tool operates at a best-effort level at converting positional
      parameters in client method calls to keyword based parameters.
      Cases where it WILL FAIL include
      A) * or ** expansion in a method call.
      B) Calls via function or method alias (includes free function calls)
      C) Indirect or dispatched calls (e.g. the method is looked up dynamically)

      These all constitute false negatives. The tool will also detect false
      positives when an API method shares a name with another method.
""")
    parser.add_argument(
        '-d',
        '--input-directory',
        required=True,
        dest='input_dir',
        help='the input directory to walk for python files to fix up',
    )
    parser.add_argument(
        '-o',
        '--output-directory',
        required=True,
        dest='output_dir',
        help='the directory to output files fixed via un-flattening',
    )
    args = parser.parse_args()
    input_dir = pathlib.Path(args.input_dir)
    output_dir = pathlib.Path(args.output_dir)
    if not input_dir.is_dir():
        print(
            f"input directory '{input_dir}' does not exist or is not a directory",
            file=sys.stderr,
        )
        sys.exit(-1)

    if not output_dir.is_dir():
        print(
            f"output directory '{output_dir}' does not exist or is not a directory",
            file=sys.stderr,
        )
        sys.exit(-1)

    if os.listdir(output_dir):
        print(
            f"output directory '{output_dir}' is not empty",
            file=sys.stderr,
        )
        sys.exit(-1)

    fix_files(input_dir, output_dir)
