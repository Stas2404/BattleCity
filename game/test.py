import unittest
from entities.Player import Player
import pygame

class TestGameEntities(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.dummy_group = pygame.sprite.Group()
        
        self.player = Player(800, 600, 
                             walls_group=self.dummy_group,
                             enemies_group=self.dummy_group,
                             all_sprites_group=self.dummy_group,
                             bullets_group=self.dummy_group,
                             enemy_bullets_group=self.dummy_group,
                             health=3)

    def test_player_initial_health(self):
        self.assertEqual(self.player.health, 3)

    def test_player_damage(self):
        self.player.health -= 1
        self.assertEqual(self.player.health, 2)

    def test_player_max_health_limit(self):
        self.player.health = 100
        self.assertEqual(self.player.health, 10)

if __name__ == '__main__':
    unittest.main()