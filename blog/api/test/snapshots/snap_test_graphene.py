# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['APITestCase::test_all_comments 1'] = {
    'data': {
        'allComments': [
        ]
    }
}

snapshots['APITestCase::test_all_posts 1'] = {
    'data': {
        'allPosts': [
        ]
    }
}

snapshots['APITestCase::test_comment 1'] = {
    'data': {
        'comment': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 9,
                    'line': 3
                }
            ],
            'message': 'Comment matching query does not exist.',
            'path': [
                'comment'
            ]
        }
    ]
}

snapshots['APITestCase::test_post 1'] = {
    'data': {
        'post': None
    },
    'errors': [
        {
            'locations': [
                {
                    'column': 9,
                    'line': 3
                }
            ],
            'message': 'Post matching query does not exist.',
            'path': [
                'post'
            ]
        }
    ]
}
